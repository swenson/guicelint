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

"""One-line documentation for opcodes module.

A detailed description of opcodes.
"""

__author__ = 'cswenson@google.com (Christopher Swenson)'

import struct

class OpcodeError(IOError): pass

class Opcode(object):
  """Base class for all Java ops"""
  def __init__(self, data, addr):
    self.opcode = ord(data[0])
    self.size = 1
  def __repr__(self):
    return str(self)

class NopOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'nop'

class PopOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'pop'

class Pop2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'pop2'

class DupOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dup'

class DupX1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dup_x1'

class DupX2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dup_x2'

class Dup2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dup2'

class Dup2X1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dup2_x1'

class Dup2X2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dup2_x2'

class SwapOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'swap'

class UnknownOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return '?(0x%02x)' % self.opcode

class LoadNullOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'aconst_null'

class ArrayLengthOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'arraylength'

class LoadIntegerM1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'iconst_m1'

class LoadInteger0Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'iconst_0'

class LoadInteger1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'iconst_1'

class LoadInteger2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'iconst_2'

class LoadInteger3Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'iconst_3'

class LoadInteger4Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'iconst_4'

class LoadInteger5Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'iconst_5'

class LoadLong0Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lconst_0'

class LoadLong1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lconst_1'

class InvokeStaticOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>H', data[1:3])[0]
  def __str__(self):
    return 'invokestatic(%d)' % self.index

class InvokeInterfaceOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 5
    self.index, self.count = struct.unpack('>HB', data[1:4])
  def __str__(self):
    return 'invokeinterface(%d, %d)' % (self.index, self.count)

class InvokeDynamicOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 5
    self.index = struct.unpack('>H', data[1:3])[0]
  def __str__(self):
    return 'invokedynamic(%d)' % (self.index)

class PutStaticOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>H', data[1:3])[0]
  def __str__(self):
    return 'putstatic(%d)' % self.index

class GetStaticOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>H', data[1:3])[0]
  def __str__(self):
    return 'getstatic(%d)' % self.index

class CheckCastOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>H', data[1:3])[0]
  def __str__(self):
    return 'checkcast(%d)' % self.index

class InstanceOfOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>H', data[1:3])[0]
  def __str__(self):
    return 'instanceof(%d)' % self.index

class MonitorEnterOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'monitorenter'

class MonitorExitOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'monitorexit'

class ReturnVoidOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'return'

class ReferenceReturnOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'areturn'

class LoadReference0Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'aload_0'

class LoadReference1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'aload_1'

class LoadReference2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'aload_2'

class LoadReference3Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'aload_3'

class GetFieldOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>H', data[1:3])[0]
  def __str__(self):
    return 'getfield(%d)' % self.index

class PutFieldOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>H', data[1:3])[0]
  def __str__(self):
    return 'putfield(%d)' % self.index

class InvokeVirtualOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>H', data[1:3])[0]
  def __str__(self):
    return 'invokevirtual(%d)' % self.index

class InvokeSpecialOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>H', data[1:3])[0]
  def __str__(self):
    return 'invokespecial(%d)' % self.index

class IfNullOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'ifnull(%d)' % self.index

class IfNotNullOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'ifnonnull(%d)' % self.index

class IfEqOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'ifeq(%d)' % self.index

class IfNeOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'ifne(%d)' % self.index

class IfLtOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'iflt(%d)' % self.index

class IfGeOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'ifge(%d)' % self.index

class IfGtOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'ifgt(%d)' % self.index

class IfLeOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'ifle(%d)' % self.index

class IfReferenceCmpEqOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'if_acmpeq(%d)' % self.index

class IfReferenceCmpNeOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'if_acmpne(%d)' % self.index

class IfIntegerCmpEqOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'if_icmpeq(%d)' % self.index

class IfIntegerCmpNeOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'if_icmpne(%d)' % self.index

class IfIntegerCmpLtOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'if_icmplt(%d)' % self.index

class IfIntegerCmpGeOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'if_icmpge(%d)' % self.index

class IfIntegerCmpGtOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'if_icmpgt(%d)' % self.index

class IfIntegerCmpLeOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'if_icmple(%d)' % self.index

class GotoOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'goto(%d)' % self.index

class GotowOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 5
    self.index = struct.unpack('>i', data[1:5])[0]
  def __str__(self):
    return 'goto_w(%d)' % self.index

class JsrOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'jsr(%d)' % self.index

class ReturnToIndexOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 2
    self.index = ord(data[1])
  def __str__(self):
    return 'ret(%d)' % self.index

class JsrwOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 5
    self.index = struct.unpack('>i', data[1:5])[0]
  def __str__(self):
    return 'jsrw(%d)' % self.index

class IntegerReturnOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'ireturn'

class LongReturnOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lreturn'

class FloatReturnOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'freturn'

class DoubleReturnOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dreturn'

class LoadArrayReferenceOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'aaload'

class LoadArrayIntegerOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'iaload'

class LoadArrayLongOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'laload'

class LoadArrayFloatOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'faload'

class LoadArrayDoubleOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'daload'

class LoadArrayBooleanOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'baload'

class LoadArrayCharacterOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'caload'

class LoadArrayShortOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'saload'

class IntegerIncrementOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index, self.const = struct.unpack('>bb', data[1:3])
  def __str__(self):
    return 'iinc(%d, %d)' % (self.index, self.const)

class LongToIntegerOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'l2i'

class LongToFloatOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'l2f'

class LongToDoubleOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'l2d'

class FloatToIntegerOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'f2i'

class FloatToLongOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'f2l'

class FloatToDoubleOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'f2d'

class DoubleToIntegerOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'd2i'

class DoubleToLongOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'd2l'

class DoubleToFloatOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'd2f'

class IntegerToLongOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'i2l'

class IntegerToFloatOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'i2f'

class IntegerToDoubleOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'i2d'

class IntegerToShortOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'i2s'

class IntegerToByteOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'i2b'

class IntegerToCharacterOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'i2c' 

class LongCmpOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lcmp'

class FloatCmpLOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fcmpl'

class FloatCmpGOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fcmpg'

class DoubleCmpLOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dcmpl'

class DoubleCmpGOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dcmpg'

class CreateNewArrayOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>H', data[1:3])[0]
  def __str__(self):
    return 'anewarray(%d)' % self.index

class CreateNewArraySizedOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 2
    self.const = ord(data[1])
  def __str__(self):
    return 'newarray(%d)' % self.const

class CreateNewMultiArrayOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 4
    self.index, self.const = struct.unpack('>HB', data[1:4])
  def __str__(self):
    return 'multianewarray(%d, %d)' % (self.index, self.const)

class NewOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>H', data[1:3])[0]
  def __str__(self):
    return 'new(%d)' % self.index

class StoreReferenceToArrayOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'aastore'

class StoreBooleanToArrayOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'bastore'

class StoreCharacterToArrayOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'castore'

class StoreShortToArrayOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'sastore'

class StoreIntegerToArrayOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'iastore'

class StoreLongToArrayOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lastore'

class StoreFloatToArrayOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fastore'

class StoreDoubleToArrayOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dastore'

class StoreReferenceIntoIndexOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 2
    self.index = ord(data[1])
  def __str__(self):
    return 'astore(%d)' % self.index

class LoadReferenceFromIndexOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 2
    self.index = ord(data[1])
  def __str__(self):
    return 'aload(%d)' % self.index

class StoreReferenceInto0Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'astore_0'

class StoreReferenceInto1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'astore_1'

class StoreReferenceInto2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'astore_2'

class StoreReferenceInto3Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'astore_3'

class PushConstantOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 2
    self.index = ord(data[1])
  def __str__(self):
    return 'ldc(%d)' % self.index

class PushShortOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.const = struct.unpack('>h', data[1:3])[0]
  def __str__(self):
    return 'sipush(%d)' % self.const

class PushByteAsIntOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 2
    self.const = struct.unpack('>b', data[1:2])[0]
  def __str__(self):
    return 'sipush(%d)' % self.const

class PushConstantWideOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>H', data[1:3])[0]
  def __str__(self):
    return 'ldc_w(%d)' % self.index

class PushConstantWideLongOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 3
    self.index = struct.unpack('>H', data[1:3])[0]
  def __str__(self):
    return 'ldc2_w(%d)' % self.index

class StoreIntegerIntoVariable0Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'istore_0'

class StoreIntegerIntoVariable1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'istore_1'

class StoreIntegerIntoVariable2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'istore_2'

class StoreIntegerIntoVariable3Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'istore_3'

class StoreIntegerIntoIndexVariableOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 2
    self.index = ord(data[1])
  def __str__(self):
    return 'istore(%d)' % self.index

class StoreLongIntoVariable0Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lstore_0'

class StoreLongIntoVariable1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lstore_1'

class StoreLongIntoVariable2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lstore_2'

class StoreLongIntoVariable3Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lstore_3'

class StoreFloatIntoVariable0Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fstore_0'

class StoreFloatIntoVariable1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fstore_1'

class StoreFloatIntoVariable2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fstore_2'

class StoreFloatIntoVariable3Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fstore_3'

class StoreDoubleIntoVariable0Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dstore_0'

class StoreDoubleIntoVariable1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dstore_1'

class StoreDoubleIntoVariable2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dstore_2'

class StoreDoubleIntoVariable3Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dstore_3'

class StoreLongIntoIndexVariableOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 2
    self.index = ord(data[1])
  def __str__(self):
    return 'lstore(%d)' % self.index

class StoreFloatIntoIndexVariableOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 2
    self.index = ord(data[1])
  def __str__(self):
    return 'fstore(%d)' % self.index

class StoreDoubleIntoIndexVariableOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 2
    self.index = ord(data[1])
  def __str__(self):
    return 'dstore(%d)' % self.index

class LoadIntegerFromIndexVariableOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 2
    self.index = ord(data[1])
  def __str__(self):
    return 'iload(%d)' % self.index

class LoadIntegerFrom0Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'iload_0'

class LoadIntegerFrom1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'iload_1'

class LoadIntegerFrom2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'iload_2'

class LoadIntegerFrom3Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'iload_3'

class LoadLongFromIndexVariableOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 2
    self.index = ord(data[1])
  def __str__(self):
    return 'lload(%d)' % self.index

class LoadLongFrom0Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lload_0'

class LoadLongFrom1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lload_1'

class LoadLongFrom2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lload_2'

class LoadLongFrom3Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lload_3'

class LoadFloatFromIndexVariableOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 2
    self.index = ord(data[1])
  def __str__(self):
    return 'fload(%d)' % self.index

class LoadFloat0Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fconst_0'

class LoadFloat1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fconst_1'

class LoadFloat2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fconst_2'

class LoadDouble0Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dconst_0'

class LoadDouble1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dconst_1'

class LoadFloatFrom0Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fload_0'

class LoadFloatFrom1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fload_1'

class LoadFloatFrom2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fload_2'

class LoadFloatFrom3Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fload_3'

class LoadDoubleFromIndexVariableOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    self.size = 2
    self.index = ord(data[1])
  def __str__(self):
    return 'dload(%d)' % self.index

class LoadDoubleFrom0Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dload_0'

class LoadDoubleFrom1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dload_1'

class LoadDoubleFrom2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dload_2'

class LoadDoubleFrom3Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dload_3'

class ThrowOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'athrow'

class IntegerAddOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'iadd'

class IntegerSubtractOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'isub'

class IntegerMultiplyOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'imul'

class IntegerDivideOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'idiv'

class LongMultiplyOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lmul'

class FloatMultiplyOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fmul'

class DoubleMultiplyOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dmul'

class LongDivideOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'ldiv'

class FloatDivideOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fdiv'

class DoubleDivideOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'ddiv'

class IntegerNegateOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'ineg'

class IntegerRemainderOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'irem'

class LongRemainderOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lrem'

class FloatRemainderOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'frem'

class DoubleRemainderOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'drem'

class LongNegateOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lneg'

class FloatNegateOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fneg'

class DoubleNegateOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dneg'

class LongAddOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'ladd'

class FloatAddOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fadd'

class DoubleAddOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dadd'

class LongSubtractOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lsub'

class FloatSubtractOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'fsub'

class DoubleSubtractOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'dsub'

class IntegerXorOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'ixor'

class LongXorOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lxor'

class IntegerShiftRightLogicalOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'iushr'

class IntegerShiftLeftOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'ishl'

class LongShiftLeftOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lshl'

class IntegerShiftRightOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'ishr'

class LongShiftRightOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lshr'

class LongShiftRightLogicalOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lushr'

class IntegerAndOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'iand'

class LongAndOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'land'

class IntegerOrOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'ior'

class LongOrOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'lor'

class TableSwitchOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    # Have to make the default align up on a 4-byte boundary.
    addr = (addr + 1) & 3
    nulls = (4 - addr) & 3
    if data[1:1 + nulls] != '\x00' * nulls:
      raise OpcodeError("Bad tableswitch opcode: not the right number of nulls")
    self.default, self.low, self.high = struct.unpack('>III', data[1 + nulls:13 + nulls])
    jumpTableSize = self.high - self.low + 1
    self.jumpTable = struct.unpack('>' + 'I' * jumpTableSize, data[13 + nulls:13 + nulls + jumpTableSize * 4])
    self.size = jumpTableSize * 4 + 12 + 1 + nulls
  def __str__(self):
    return 'tableswitch' + str((self.default, self.low, self.high) + self.jumpTable)

class LookupSwitchOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    # Have to make the default align up on a 4-byte boundary.
    addr = (addr + 1) & 3
    nulls = (4 - addr) & 3
    if data[1:1 + nulls] != '\x00' * nulls:
      raise OpcodeError("Bad tableswitch opcode: not the right number of nulls")
    self.default, numPairs = struct.unpack('>II', data[1 + nulls:9 + nulls])
    self.pairs = struct.unpack('>' + 'I' * (numPairs * 2), data[9 + nulls:9 + nulls + numPairs * 8])
    self.size = numPairs * 8 + 8 + 1 + nulls
  def __str__(self):
    return 'lookupswitch' + str((self.default, ) + self.pairs)

class WideOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
    # Widen the next load/store/ret/iinc.
    # iinc is special -- 5 bytes
    if opcodeTable[data[1]] == IntegerIncrementOpcode:
      iinc = IntegerIncrementOpcode(data[1:4], addr + 1)
      iinc.index, iinc.const = struct.unpack('>HH', data[2:6])
      iinc.size = 5
      self.op = iinc
    else:
      self.op = opcodeTable[data[1]](data[1:3], addr + 1)
      self.op.index = struct.unpack('>H', data[2:4])[0]
      self.op.size = 3
    self.size = self.op.size + 1
  def __str__(self):
    return 'wide ' + str(self.op)

class BreakpointOpcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'breakpoint'

class ImplementationDependentDebugger1Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'impdep1'

class ImplementationDependentDebugger2Opcode(Opcode):
  def __init__(self, data, addr):
    Opcode.__init__(self, data, addr)
  def __str__(self):
    return 'impdep2'


opcodeTable = {}
for i in xrange(256):
  opcodeTable[i] = UnknownOpcode
opcodeTable[0x00] = NopOpcode
opcodeTable[0x01] = LoadNullOpcode
opcodeTable[0x02] = LoadIntegerM1Opcode
opcodeTable[0x03] = LoadInteger0Opcode
opcodeTable[0x04] = LoadInteger1Opcode
opcodeTable[0x05] = LoadInteger2Opcode
opcodeTable[0x06] = LoadInteger3Opcode
opcodeTable[0x07] = LoadInteger4Opcode
opcodeTable[0x08] = LoadInteger5Opcode
opcodeTable[0x09] = LoadLong0Opcode
opcodeTable[0x0a] = LoadLong1Opcode
opcodeTable[0x0b] = LoadFloat0Opcode
opcodeTable[0x0c] = LoadFloat1Opcode
opcodeTable[0x0d] = LoadFloat2Opcode
opcodeTable[0x0e] = LoadDouble0Opcode
opcodeTable[0x0f] = LoadDouble1Opcode
opcodeTable[0x10] = PushByteAsIntOpcode
opcodeTable[0x11] = PushShortOpcode
opcodeTable[0x12] = PushConstantOpcode
opcodeTable[0x13] = PushConstantWideOpcode
opcodeTable[0x14] = PushConstantWideLongOpcode
opcodeTable[0x15] = LoadIntegerFromIndexVariableOpcode
opcodeTable[0x16] = LoadLongFromIndexVariableOpcode
opcodeTable[0x17] = LoadFloatFromIndexVariableOpcode
opcodeTable[0x18] = LoadDoubleFromIndexVariableOpcode
opcodeTable[0x19] = LoadReferenceFromIndexOpcode
opcodeTable[0x1a] = LoadIntegerFrom0Opcode
opcodeTable[0x1b] = LoadIntegerFrom1Opcode
opcodeTable[0x1c] = LoadIntegerFrom2Opcode
opcodeTable[0x1d] = LoadIntegerFrom3Opcode
opcodeTable[0x1e] = LoadLongFrom0Opcode
opcodeTable[0x1f] = LoadLongFrom1Opcode
opcodeTable[0x20] = LoadLongFrom2Opcode
opcodeTable[0x21] = LoadLongFrom3Opcode
opcodeTable[0x22] = LoadFloatFrom0Opcode
opcodeTable[0x23] = LoadFloatFrom1Opcode
opcodeTable[0x24] = LoadFloatFrom2Opcode
opcodeTable[0x25] = LoadFloatFrom3Opcode
opcodeTable[0x26] = LoadDoubleFrom0Opcode
opcodeTable[0x27] = LoadDoubleFrom1Opcode
opcodeTable[0x28] = LoadDoubleFrom2Opcode
opcodeTable[0x29] = LoadDoubleFrom3Opcode
opcodeTable[0x2a] = LoadReference0Opcode
opcodeTable[0x2b] = LoadReference1Opcode
opcodeTable[0x2c] = LoadReference2Opcode
opcodeTable[0x2d] = LoadReference3Opcode
opcodeTable[0x2e] = LoadArrayIntegerOpcode
opcodeTable[0x2f] = LoadArrayLongOpcode
opcodeTable[0x30] = LoadArrayFloatOpcode
opcodeTable[0x31] = LoadArrayDoubleOpcode
opcodeTable[0x32] = LoadArrayReferenceOpcode
opcodeTable[0x33] = LoadArrayBooleanOpcode
opcodeTable[0x34] = LoadArrayCharacterOpcode
opcodeTable[0x35] = LoadArrayShortOpcode
opcodeTable[0x36] = StoreIntegerIntoIndexVariableOpcode
opcodeTable[0x37] = StoreLongIntoIndexVariableOpcode
opcodeTable[0x38] = StoreFloatIntoIndexVariableOpcode
opcodeTable[0x39] = StoreDoubleIntoIndexVariableOpcode
opcodeTable[0x3a] = StoreReferenceIntoIndexOpcode
opcodeTable[0x3b] = StoreIntegerIntoVariable0Opcode
opcodeTable[0x3c] = StoreIntegerIntoVariable1Opcode
opcodeTable[0x3d] = StoreIntegerIntoVariable2Opcode
opcodeTable[0x3e] = StoreIntegerIntoVariable3Opcode
opcodeTable[0x3f] = StoreLongIntoVariable0Opcode
opcodeTable[0x40] = StoreLongIntoVariable1Opcode
opcodeTable[0x41] = StoreLongIntoVariable2Opcode
opcodeTable[0x42] = StoreLongIntoVariable3Opcode
opcodeTable[0x43] = StoreFloatIntoVariable0Opcode
opcodeTable[0x44] = StoreFloatIntoVariable1Opcode
opcodeTable[0x45] = StoreFloatIntoVariable2Opcode
opcodeTable[0x46] = StoreFloatIntoVariable3Opcode
opcodeTable[0x47] = StoreDoubleIntoVariable0Opcode
opcodeTable[0x48] = StoreDoubleIntoVariable1Opcode
opcodeTable[0x49] = StoreDoubleIntoVariable2Opcode
opcodeTable[0x4a] = StoreDoubleIntoVariable3Opcode
opcodeTable[0x4b] = StoreReferenceInto0Opcode
opcodeTable[0x4c] = StoreReferenceInto1Opcode
opcodeTable[0x4d] = StoreReferenceInto2Opcode
opcodeTable[0x4e] = StoreReferenceInto3Opcode
opcodeTable[0x4f] = StoreIntegerToArrayOpcode
opcodeTable[0x50] = StoreLongToArrayOpcode
opcodeTable[0x51] = StoreFloatToArrayOpcode
opcodeTable[0x52] = StoreDoubleToArrayOpcode
opcodeTable[0x53] = StoreReferenceToArrayOpcode
opcodeTable[0x54] = StoreBooleanToArrayOpcode
opcodeTable[0x55] = StoreCharacterToArrayOpcode
opcodeTable[0x56] = StoreShortToArrayOpcode
opcodeTable[0x57] = PopOpcode
opcodeTable[0x58] = Pop2Opcode
opcodeTable[0x59] = DupOpcode
opcodeTable[0x5a] = DupX1Opcode
opcodeTable[0x5b] = DupX2Opcode
opcodeTable[0x5c] = Dup2Opcode
opcodeTable[0x5d] = Dup2X1Opcode
opcodeTable[0x5e] = Dup2X2Opcode
opcodeTable[0x5f] = SwapOpcode
opcodeTable[0x60] = IntegerAddOpcode
opcodeTable[0x61] = LongAddOpcode
opcodeTable[0x62] = FloatAddOpcode
opcodeTable[0x63] = DoubleAddOpcode
opcodeTable[0x64] = IntegerSubtractOpcode
opcodeTable[0x65] = LongSubtractOpcode
opcodeTable[0x66] = FloatSubtractOpcode
opcodeTable[0x67] = DoubleSubtractOpcode
opcodeTable[0x68] = IntegerMultiplyOpcode
opcodeTable[0x69] = LongMultiplyOpcode
opcodeTable[0x6a] = FloatMultiplyOpcode
opcodeTable[0x6b] = DoubleMultiplyOpcode
opcodeTable[0x6c] = IntegerDivideOpcode
opcodeTable[0x6d] = LongDivideOpcode
opcodeTable[0x6e] = FloatDivideOpcode
opcodeTable[0x6f] = DoubleDivideOpcode
opcodeTable[0x70] = IntegerRemainderOpcode
opcodeTable[0x71] = LongRemainderOpcode
opcodeTable[0x72] = FloatRemainderOpcode
opcodeTable[0x73] = DoubleRemainderOpcode
opcodeTable[0x74] = IntegerNegateOpcode
opcodeTable[0x75] = LongNegateOpcode
opcodeTable[0x76] = FloatNegateOpcode
opcodeTable[0x77] = DoubleNegateOpcode
opcodeTable[0x78] = IntegerShiftLeftOpcode
opcodeTable[0x79] = LongShiftLeftOpcode
opcodeTable[0x7a] = IntegerShiftRightOpcode
opcodeTable[0x7b] = LongShiftRightOpcode
opcodeTable[0x7c] = IntegerShiftRightLogicalOpcode
opcodeTable[0x7d] = LongShiftRightLogicalOpcode
opcodeTable[0x7e] = IntegerAndOpcode
opcodeTable[0x7f] = LongAndOpcode
opcodeTable[0x80] = IntegerOrOpcode
opcodeTable[0x81] = LongOrOpcode
opcodeTable[0x82] = IntegerXorOpcode
opcodeTable[0x83] = LongXorOpcode
opcodeTable[0x84] = IntegerIncrementOpcode
opcodeTable[0x85] = IntegerToLongOpcode
opcodeTable[0x86] = IntegerToFloatOpcode
opcodeTable[0x87] = IntegerToDoubleOpcode
opcodeTable[0x88] = LongToIntegerOpcode
opcodeTable[0x89] = LongToFloatOpcode
opcodeTable[0x8a] = LongToDoubleOpcode
opcodeTable[0x8b] = FloatToIntegerOpcode
opcodeTable[0x8c] = FloatToLongOpcode
opcodeTable[0x8d] = FloatToDoubleOpcode
opcodeTable[0x8e] = DoubleToIntegerOpcode
opcodeTable[0x8f] = DoubleToLongOpcode
opcodeTable[0x90] = DoubleToFloatOpcode
opcodeTable[0x91] = IntegerToByteOpcode
opcodeTable[0x92] = IntegerToCharacterOpcode
opcodeTable[0x93] = IntegerToShortOpcode
opcodeTable[0x94] = LongCmpOpcode
opcodeTable[0x95] = FloatCmpLOpcode
opcodeTable[0x96] = FloatCmpGOpcode
opcodeTable[0x97] = DoubleCmpLOpcode
opcodeTable[0x98] = DoubleCmpGOpcode
opcodeTable[0x99] = IfEqOpcode
opcodeTable[0x9a] = IfNeOpcode
opcodeTable[0x9b] = IfLtOpcode
opcodeTable[0x9c] = IfGeOpcode
opcodeTable[0x9d] = IfGtOpcode
opcodeTable[0x9e] = IfLeOpcode
opcodeTable[0x9f] = IfIntegerCmpEqOpcode
opcodeTable[0xa0] = IfIntegerCmpNeOpcode
opcodeTable[0xa1] = IfIntegerCmpLtOpcode
opcodeTable[0xa2] = IfIntegerCmpGeOpcode
opcodeTable[0xa3] = IfIntegerCmpGtOpcode
opcodeTable[0xa4] = IfIntegerCmpLeOpcode
opcodeTable[0xa5] = IfReferenceCmpEqOpcode
opcodeTable[0xa6] = IfReferenceCmpNeOpcode
opcodeTable[0xa7] = GotoOpcode
opcodeTable[0xa8] = JsrOpcode
opcodeTable[0xa9] = ReturnToIndexOpcode
opcodeTable[0xaa] = TableSwitchOpcode
opcodeTable[0xab] = LookupSwitchOpcode
opcodeTable[0xac] = IntegerReturnOpcode
opcodeTable[0xad] = LongReturnOpcode
opcodeTable[0xae] = FloatReturnOpcode
opcodeTable[0xaf] = DoubleReturnOpcode
opcodeTable[0xb0] = ReferenceReturnOpcode
opcodeTable[0xb1] = ReturnVoidOpcode
opcodeTable[0xb2] = GetStaticOpcode
opcodeTable[0xb3] = PutStaticOpcode
opcodeTable[0xb4] = GetFieldOpcode
opcodeTable[0xb5] = PutFieldOpcode
opcodeTable[0xb6] = InvokeVirtualOpcode
opcodeTable[0xb7] = InvokeSpecialOpcode
opcodeTable[0xb8] = InvokeStaticOpcode
opcodeTable[0xb9] = InvokeInterfaceOpcode
opcodeTable[0xba] = InvokeDynamicOpcode
opcodeTable[0xbb] = NewOpcode
opcodeTable[0xbc] = CreateNewArraySizedOpcode
opcodeTable[0xbd] = CreateNewArrayOpcode
opcodeTable[0xbe] = ArrayLengthOpcode
opcodeTable[0xbf] = ThrowOpcode
opcodeTable[0xc0] = CheckCastOpcode
opcodeTable[0xc1] = InstanceOfOpcode
opcodeTable[0xc2] = MonitorEnterOpcode
opcodeTable[0xc3] = MonitorExitOpcode
opcodeTable[0xc4] = WideOpcode
opcodeTable[0xc5] = CreateNewMultiArrayOpcode
opcodeTable[0xc6] = IfNullOpcode
opcodeTable[0xc7] = IfNotNullOpcode
opcodeTable[0xc8] = GotowOpcode
opcodeTable[0xc9] = JsrwOpcode
opcodeTable[0xca] = BreakpointOpcode
opcodeTable[0xfe] = ImplementationDependentDebugger1Opcode
opcodeTable[0xff] = ImplementationDependentDebugger2Opcode
