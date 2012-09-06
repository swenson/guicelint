# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""guice_lint is a program for finding Guice errors.

Finds mismatches between @Provides and @Inject usages.
"""

__author__ = 'cswenson@google.com (Christopher Swenson)'

import struct
import zipfile

from opcodes import opcodeTable
from collections import namedtuple

Constant = namedtuple('Constant', 'type value')
Field = namedtuple('Field', 'accessFlags nameIndex descriptorIndex attributes')
Method = namedtuple('Method', 'accessFlags nameIndex descriptorIndex attributes'
                    ' code')
Attribute = namedtuple('Attribute', 'index info annotations parameterAnnotations')
JavaException = namedtuple('JavaException', 'startPc endPc handlerPc catchType')
Code = namedtuple('Code', 'maxStack maxLocals code exceptions attributes')
Annotation = namedtuple('Annotation', 'typeIndex pairs')

# Global table of .class files parsed.
loadedClasses = {}

def main(argv):
  global jar
  jar = zipfile.ZipFile(open(argv[1]))
  global namelist
  namelist = set(jar.namelist())
  manifest = jar.open('META-INF/MANIFEST.MF').read()
  mainClass = GetMain(manifest)
  fname = FindFile(mainClass)
  classFile = LoadClass(fname)
  for m in classFile.methods:
    name = classFile.constants[m.nameIndex].value
    if name == 'main':
      providers, injected = classFile.GetProvidersAndInjectors(m)
      stillNeeded = set(injected) - set(providers)
      if stillNeeded:
        print "Error! Could not resolve the following injections:"
        for x in sorted(stillNeeded):
          if x[1] is not None:
            print '  Named(%s) %s' % (x[1], x[0])
          else:
            print '  ' + str(x[0])
        exit(1)

def LoadClass(fname):
  if fname in loadedClasses:
    return loadedClasses[fname]
  classFile = JavaClassFile(jar.open(fname))
  loadedClasses[fname] = classFile
  return classFile

def GetMain(manifest):
  for l in manifest.split('\n'):
    l = l.strip()
    if ':' not in l: continue
    parts = l.split(':')
    if parts[0].strip() != 'Main-Class': continue
    return parts[1].strip()

def FindFile(className):
  className = className.replace('.', '/')
  className += '.class'
  if className in namelist:
    return className

def ReadConstant(data):
  tag = ord(data[0])
  length = 0
  if tag == 1:
    length = struct.unpack('>H', data[1:3])[0]
    string = data[3:3 + length]
    return Constant('str', string), 1, 3 + length
  elif tag == 5:
    value = struct.unpack('>q', data[1:9])[0]
    return Constant('long', value), 2, 9
  elif tag == 6:
    value = struct.unpack('>d', data[1:9])[0]
    return Constant('double', value), 2, 9
  elif tag == 3:
    value = struct.unpack('>i', data[1:5])[0]
    return Constant('int', value), 1, 5
  elif tag == 4:
    value = struct.unpack('>f', data[1:5])[0]
    return Constant('float', value), 1, 5
  elif tag == 9:
    v1, v2 = struct.unpack('>HH', data[1:5])
    return Constant('fieldref', (v1, v2)), 1, 5
  elif tag == 10:
    v1, v2 = struct.unpack('>HH', data[1:5])
    return Constant('methodref', (v1, v2)), 1, 5
  elif tag == 11:
    v1, v2 = struct.unpack('>HH', data[1:5])
    return Constant('interfacemethodref', (v1, v2)), 1, 5
  elif tag == 12:
    v1, v2 = struct.unpack('>HH', data[1:5])
    return Constant('nametypedescriptor', (v1, v2)), 1, 5
  elif tag == 7:
    value = struct.unpack('>H', data[1:3])[0]
    return Constant('classref', value), 1, 3
  elif tag == 8:
    value = struct.unpack('>H', data[1:3])[0]
    return Constant('stringref', value), 1, 3

def Disassemble(data):
  """Number 5 alive."""
  ops = []
  d = data
  addr = 0
  while d:
    op, skip = ReadOpcode(d, addr)
    ops.append(op)
    d = d[skip:]
    addr += skip
  return tuple(ops)

def ReadOpcode(data, addr):
  opcode = ord(data[0])
  op = opcodeTable[opcode](data, addr)
  return op, op.size


class JavaClassFile(object):
  def __init__(self, fileLike):
    self.data = fileLike.read()
    self.ReadHeader()
    self.ReadConstants()
    self.ReadHeader2()
    self.ReadInterfaces()
    self.ReadFields()
    self.ReadMethods()
    self.ReadClassAttributes()

  def ReadHeader(self):
    headerBytes = self.data[:10]
    self.data = self.data[10:]
    assert headerBytes[:4] == '\xCA\xFE\xBA\xBE'
    _, self.minor, self.major, self.constantPoolCount = \
        struct.unpack('>iHHH', headerBytes)
  def ReadConstants(self):
    i = 1
    constants = [None]
    classes = []
    while i < self.constantPoolCount:
      constant, slots, skip = ReadConstant(self.data)
      if constant[0] == 'classref':
        classes.append(i)
      self.data = self.data[skip:]
      constants.append(constant)
      if slots == 2:
        constants.append(None)
      i += slots
    self.constants = constants
    self.classes = {}
    for i in classes:
      self.classes[self.constants[self.constants[i].value].value] = i

  def ReadHeader2(self):
    self.accessFlags, self.classIndex, self.superIndex, self.interfaceCount = \
        struct.unpack('>HHHH', self.data[:8])
    self.data = self.data[8:]

  def ReadInterfaces(self):
    self.interfaces = []
    for i in xrange(self.interfaceCount):
      self.interfaces.append(struct.unpack('>H',
          self.data[2 * i:2 * i + 2])[0])
    self.data = self.data[self.interfaceCount * 2:]

  def ReadFields(self):
    self.fieldCount = struct.unpack('>H', self.data[:2])[0]
    self.fields = []
    self.data = self.data[2:]
    for _ in xrange(self.fieldCount):
      field, skip = self.ReadField(self.data)
      self.fields.append(field)
      self.data = self.data[skip:]

  def ReadMethods(self):
    self.namedMethods = {}
    self.methodCount = struct.unpack('>H', self.data[:2])[0]
    self.data = self.data[2:]
    self.methods = []
    for _ in xrange(self.methodCount):
      method, skip = self.ReadMethod(self.data)
      self.data = self.data[skip:]
      method = self.FindCode(method)
      name = self.constants[method.nameIndex].value
      if name in self.namedMethods:
        self.namedMethods[name].append(method)
      else:
        self.namedMethods[name] = [method]
      self.methods.append(method)

  def ReadClassAttributes(self):
    count = struct.unpack('>H', self.data[:2])[0]
    self.classAttributes = self.ReadAttributes(self.data[2:], count)
    del self.data

  def FindCode(self, method):
    code = None
    for attribute in method.attributes:
      constant = self.constants[attribute.index]
      if constant.value == 'Code':
        code = self.ReadCode(attribute.info)
        break
    return Method(method.accessFlags, method.nameIndex, method.descriptorIndex,
                  method.attributes, code)
  def ReadAttributes(self, data, count):
    offset = 0
    attributes = []
    for _ in xrange(count):
      index, count = struct.unpack('>HI', data[offset:offset + 6])
      name = self.constants[index].value
      info = data[offset + 6:offset + 6 + count]
      offset += 6 + count
      annotations = None
      parameterAnnotations = None
      if name == 'RuntimeVisibleAnnotations':
        annotations = self.GetAnnotations(info)
      elif name == 'RuntimeVisibleParameterAnnotations':
        parameterAnnotations = self.GetParameterAnnotations(info)

      attributes.append(Attribute(index, info, annotations, parameterAnnotations))
    return attributes, offset

  def GetAnnotations(self, info):
    numAnnotations = struct.unpack('>H', info[:2])[0]
    info = info[2:]
    annotations = []
    for _ in xrange(numAnnotations):
      annotation, skip = self.ReadAnnotation(info)
      info = info[skip:]
      annotations.append(annotation)
    return annotations

  def GetParameterAnnotations(self, info):
    numParameters = ord(info[0])
    info = info[1:]
    parameters = []
    for i in xrange(numParameters):
      annotations = []
      numAnnotations = struct.unpack('>H', info[:2])[0]
      info = info[2:]
      for _ in xrange(numAnnotations):
        annotation, skip = self.ReadAnnotation(info)
        info = info[skip:]
        annotations.append(annotation)
      parameters.append(tuple(annotations))
    return tuple(parameters)

  def ReadAnnotation(self, info):
    typeIndex, numPairs = struct.unpack('>HH', info[:4])
    baseType = ParseBaseType(self.constants[typeIndex].value)
    info = info[4:]
    pairs = []
    size = 4
    for _ in xrange(numPairs):
      elementNameIndex = struct.unpack('>H', info[:2])[0]
      size += 2
      info = info[2:]
      value, skip = self.ReadElementValue(info)
      info = info[skip:]
      size += skip
      pairs.append((elementNameIndex, value))
    return Annotation(baseType, pairs), size

  def ReadElementValue(self, info):
    tag = info[0]
    if tag not in 'BCDFIJSZ@[ecs':
      exit("Parsing error: unknown tag %s (%d) found in elementValue" % (tag,
                                                                         ord(tag)))
    if tag == '@':
      annotation, skip = self.ReadAnnotation(self, info[1:])
      skip += 1
      return ((tag, annotation), skip)
    elif tag == '[':
      size = 3
      numValues = struct.unpack('>H', info[1:3])[0]
      info = info[3:]
      values = []
      for _ in xrange(numValues):
        value, skip = self.ReadElementValue(info)
        info = info[skip:]
        size += skip
        values.append(value)
      return ((tag, values), size)
    elif tag == 'e':
      value = struct.unpack('>HH', info[1:5])
      return ((tag, value), 5)
    value = struct.unpack('>H', info[1:3])[0]
    return ((tag, value), 3)

  def ReadField(self, data):
    accessFlags, nameIndex, descriptorIndex, attributesCount = \
        struct.unpack('>HHHH', data[:8])
    attributes, skip = self.ReadAttributes(data[8:], attributesCount)
    return Field(accessFlags, nameIndex, descriptorIndex, attributes), skip + 8

  def ReadMethod(self, data):
    accessFlags, nameIndex, descriptorIndex, attributesCount = \
        struct.unpack('>HHHH', data[:8])
    attributes, skip = self.ReadAttributes(data[8:], attributesCount)
    return Method(accessFlags, nameIndex, descriptorIndex, attributes, None), skip + 8

  def ReadCode(self, attr):
    maxStack, maxLocals, codeLength = struct.unpack('>HHI', attr[:8])
    code = Disassemble(attr[8:8 + codeLength])
    exceptionTableLength = struct.unpack('>H', attr[8 + codeLength: 10 +
                                                    codeLength])[0]
    exceptions = []
    for i in xrange(exceptionTableLength):
      startPc, endPc, handlerPc, catchType = struct.unpack('>HHHH',
          attr[10 + codeLength + i * 8:10 + codeLength + i * 8 + 8])
      exceptions.append(JavaException(startPc, endPc, handlerPc, catchType))

    attributesCount = struct.unpack('>H', attr[10 + codeLength + exceptionTableLength * 8:10 + codeLength + exceptionTableLength * 8 +
                                               2])[0]
    attributes = self.ReadAttributes(attr[10 + codeLength + exceptionTableLength * 8
                                     + 2:], attributesCount)
    return Code(maxStack, maxLocals, code, exceptions, attributes)

  def GetProvidersAndInjectors(self, method):
    # Go 3 deep:
    methodName = self.constants[method.nameIndex].value
    classRef = self.constants[self.classIndex]
    className = self.constants[classRef.value].value
    calledMethods, injected = self.GetAllCalled([className + '.' + methodName])
    fanout = [calledMethods]
    while len(fanout) < 3:
      newMethods, injectedClasses = self.GetAllCalled(fanout[-1])
      fanout.append(newMethods)
      injected += injectedClasses
    allCalled = set()
    for x in fanout:
      allCalled = allCalled.union(set(x))
    modules = self.FindModules(allCalled)
    providers = self.FindAllProviders(modules)
    newProviders, newInjected = self.FindAllBindings(modules)
    providers += newProviders
    injected += newInjected
    newProviders, newInjected = InjectedTransitiveClosure(injected)
    providers += newProviders
    return providers, newInjected

  def FindAllBindings(self, modules):
    providers = []
    injected = []
    done = set()
    while modules:
      module = modules.pop()
      if module in done:
        continue
      newProviders, newInjected, newModules = self.FindBindings(module)
      providers += newProviders
      providers += self.FindProviders(module)
      modules += newModules
      injected += newInjected
      done.add(module)
    return providers, injected

  def FindBindings(self, module):
    classFile = LoadClass(FindFile(module))
    providers = []
    injectors = []
    newModules = []
    for method in classFile.methods:
      if classFile.constants[method.nameIndex].value != 'configure':
        continue
      prev = None
      to = None
      for op in method.code.code:
        call = classFile.IsCall(op)
        if call is not None:
          if call.endswith('.install'):
            modCall = classFile.IsCall(prev)
            if modCall is not None:
              if '.' in modCall:
                modCall = modCall[:modCall.index('.')]
              newModules.append(modCall)
          if call.endswith('.bind'):
            if str(prev).startswith('ldc'):
              bind = classFile.constants[classFile.constants[prev.index].value].value
          if call == 'com/google/inject/binder/AnnotatedBindingBuilder.to':
            providers.append((bind, None))
            if str(prev).startswith('ldc'):
              to = classFile.constants[classFile.constants[prev.index].value].value
              injectors.append((to, None))
          if call == 'com/google/inject/binder/AnnotatedBindingBuilder.toInstance':
            providers.append((bind, None))
        prev = op
    return providers, injectors, newModules

  def FindAllProviders(self, modules):
    providers = []
    for module in modules:
      providers += self.FindProviders(module)
    return providers

  def FindProviders(self, module):
    classFile = LoadClass(FindFile(module))
    providers = []
    for method in classFile.methods:
      provides = None
      named = None
      for attribute in method.attributes:
        if attribute.annotations is not None:
          for annotation in attribute.annotations:
            if annotation.typeIndex[0] == ('L', 'com/google/inject/Provides'):
              provides = classFile.constants[method.descriptorIndex].value
            elif annotation.typeIndex[0] == ('L', 'com/google/inject/name/Named'):
              named = classFile.constants[annotation.pairs[0][1][1]].value
      if provides is not None:
        provides = GetReturnType(provides)
        providers.append((provides, named))
    return providers

  def FindModules(self, methodNames):
    modules = []
    for methodName in methodNames:
      fname, mname = methodName.split('.')
      f = FindFile(fname)
      if not f:
        continue
      otherClass = LoadClass(FindFile(fname))
      if mname not in otherClass.namedMethods:
        continue
      superClass = otherClass.constants[otherClass.constants[otherClass.superIndex].value].value
      if superClass == 'com/google/inject/AbstractModule':
        modules.append(fname)
    return modules

  def GetAllCalled(self, methodNames):
    called = []
    injected = []
    for methodName in methodNames:
      fname, mname = methodName.split('.')
      f = FindFile(fname)
      if not f:
        continue
      otherClass = LoadClass(FindFile(fname))
      if mname not in otherClass.namedMethods:
        continue
      otherMethods = otherClass.namedMethods[mname]
      for otherMethod in otherMethods:
        newCalled = otherClass.GetCalled(otherMethod)
        if 'com/google/inject/Injector.getInstance' in newCalled:
          injected += otherClass.GetInjected(otherMethod)
        called += newCalled
    return called, injected

  def GetInjected(self, method):
    injected = []
    prev = None
    for x in method.code.code:
      c = self.IsCall(x)
      if c == 'com/google/inject/Injector.getInstance':
        if str(prev).startswith('ldc'):
          injected.append((self.constants[self.constants[prev.index].value].value,
                           None))
      prev = x
    return injected

  def GetCalled(self, method):
    called = []
    if not method.code:
      return called
    for x in method.code.code:
      c = self.IsCall(x)
      if c:
        called.append(c)
    return called

  def IsCall(self, x):
    if str(x).startswith('invoke'):
      c = self.constants[x.index]
      classRef = self.constants[c.value[0]]
      calling = self.constants[classRef.value].value
      calling += '.'
      descRef = self.constants[c.value[1]]
      name = self.constants[descRef.value[0]]
      calling += name.value
      type = self.constants[descRef.value[1]]
      return calling
  def FindClass(self, className):
    if className not in self.classes:
      return None
    return self.classes[className]

def GetReturnType(s):
  returnType = ParseBaseType(s[s.index(')') + 1:])
  return BaseTypeClass(returnType[0])

def BaseTypeClass(x):
  if x[0] == 'L':
    return x[1]
  if x[0] == 'B':
    return 'java/lang/Byte'
  elif x[0] == 'C':
    return 'java/lang/Character'
  elif x[0] == 'D':
    return 'java/lang/Double'
  elif x[0] == 'F':
    return 'java/lang/Float'
  elif x[0] == 'I':
    return 'java/lang/Integer'
  elif x[0] == 'J':
    return 'java/lang/Long'
  elif x[0] == 'S':
    return 'java/lang/Short'
  elif x[0] == 'Z':
    return 'java/lang/Boolean'
  elif x[0] == '[':
    # TODO(cswenson): Support injection of named arrays.
    return None
  return None


def GetArgumentClasses(s, parameterAnnotations, classFile):
  s = s[s.index('(') + 1:s.index(')')]
  types = ParseBaseTypes(s)
  args = []
  for i, x in enumerate(types):
    named = None
    if parameterAnnotations is not None:
      for annotation in parameterAnnotations[i]:
        if annotation.typeIndex[0] == ('L', 'com/google/inject/name/Named'):
          named = classFile.constants[annotation.pairs[0][1][1]].value
    if x[0] == 'L':
      args.append((x[1], named))
    elif named is not None:
      t = BaseTypeClass(x)
      if t is not None:
        args.append((t, named))
  return args

def ParseBaseTypes(s):
  types = []
  while s:
    type, skip = ParseBaseType(s)
    s = s[skip:]
    types.append(type)
  return types

def ParseBaseType(s):
  tag = s[0]
  if tag == 'L':
    name = s[1:s.index(';')]
    type = (tag, name)
    return type, 2 + len(name)
  if tag == '[':
    levels = 0
    while tag == '[':
      levels += 1
      s = s[1:]
      tag = s[0]
    type, skip = ParseBaseType(s)
    return ('[' * levels + type[0], type[1]), skip + levels
  else:
    return (tag, None), 1


def InjectedTransitiveClosure(injected):
  newClasses = []
  providers = []
  done = set()
  todo = injected[:]
  while todo:
    className, name = todo.pop()
    if (className, name) in done:
      continue
    done.add((className, name))
    newClasses.append((className, name))
    fname = FindFile(className)
    if not fname:
      continue
    classFile = LoadClass(fname)
    classRef = classFile.FindClass(className)
    if classRef is None: continue
    foundAnnotation = False
    for method in classFile.methods:
      methodName = classFile.constants[method.nameIndex].value
      if methodName != '<init>':
        continue
      # Guice will inject argument-less constructurs.
      if classFile.constants[method.descriptorIndex].value == '()V':
        providers.append((className, None))
        break

      methodAnnotations = None
      parameterAnnotations = None
      for attribute in method.attributes:
        if attribute.parameterAnnotations is not None:
          parameterAnnotations = attribute.parameterAnnotations
        if attribute.annotations is not None:
          methodAnnotations = attribute.annotations
        if parameterAnnotations is not None and methodAnnotations is not None:
          break
      if methodAnnotations is not None:
        for annotation in methodAnnotations:
          if annotation.typeIndex[0][1] == 'com/google/inject/Inject':
            foundAnnotation = True
            providers.append((className, None))
            argClasses = GetArgumentClasses(classFile.constants[method.descriptorIndex].value, parameterAnnotations, classFile)
            # Don't include Injector, etc.
            argClasses = [x for x in argClasses if not x[0].startswith('com/google/inject')]
            # TODO(cswenson): Read annotations for @Named in arguments.
            newClasses += argClasses
            todo += argClasses
            break
    if not foundAnnotation:
      continue
    # Check fields for @Inject, and for superclasses.
    newClasses += FindInjectedFields(className)
    todo += newClasses

  return providers, newClasses

def FindInjectedFields(className):
  classFile = LoadClass(FindFile(className))
  needed = []
  for field in classFile.fields:
    for attribute in field.attributes:
      if attribute.annotations is None:
        continue
      bind = None
      named = None
      for annotation in attribute.annotations:
        if annotation.typeIndex[0][1] == 'com/google/inject/Inject':
          desc = classFile.constants[field.descriptorIndex].value
          bind = ParseBaseType(desc)[0][1]
          needed.append((bind, None))
        elif annotation.typeIndex[0] == ('L', 'com/google/inject/name/Named'):
          named = classFile.constants[annotation.pairs[0][1][1]].value
          needed[-1] = (bind, named)
  superClass = classFile.constants[classFile.constants[classFile.superIndex].value].value
  if superClass.startswith('java'):
    return needed
  needed += FindInjectedFields(superClass)
  return needed



if __name__ == '__main__':
  import sys
  main(sys.argv)
