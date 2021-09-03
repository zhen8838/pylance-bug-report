import bitstruct
from typing import *
import binascii
from enum import Enum

HookProperty = property

class serialize_struct():
  def __init__(self,hooks = None):
    pass

class datatype(Enum):
  int8 = 0x00
  int16 = 0x01
  int32 = 0x02
  int64 = 0x03
  uint8 = 0x04
  uint16 = 0x05
  uint32 = 0x06
  uint64 = 0x07
  float16 = 0x08
  float32 = 0x09
  float64 = 0x0A
  bfloat16 = 0x0B


class ADDR(int):

    def __repr__(self) -> str:
        return "0x%x" % self


class REG(int):
    pass


class ADDR_GLB:
    align: bool
    has_bank: bool
    value: int

    def __init__(self, align: bool, has_bank: bool):
        self.align = align
        self.has_bank = has_bank

    def __int__(self):
        return self.value

    @property
    def bank(self) -> int:
        if self.has_bank:
            if self.align:
                raise Exception("not support")
            else:
                val = self.value >> 21
                assert 16 > val >= 0
                return val
        else:
            return 0

    @bank.setter
    def bank(self, val: int):
        assert val < 16
        assert val >= 0
        assert self.has_bank
        if self.align:
            raise Exception("not support")
        else:
            self.value = (self.value & 0x1FFFFF) | (val << 21)

    @property
    def addr(self) -> int:
        if self.align:
            raise Exception("not support")
        else:
            return self.value & 0x1FFFFF

    @addr.setter
    def addr(self, addr: int):
        if self.align:
            raise Exception("not support")
        else:
            assert addr < (1 << 21)
            self.value = (self.value & (0xF << 21)) | addr

    def get_addr(self):
        return self.addr

    def get_bank(self):
        return self.bank

    def set_addr(self, value: int):
        self.addr = value
        return self

    def set_bank(self, value: int):
        self.bank = value
        return self


class ADDR_GLB_8_WITHOUT_BANK(ADDR_GLB):

    def __init__(self, value: int = 0):
        super().__init__(False, False)
        self.value = int(value)

    def __repr__(self) -> str:
        return "ADDR_GLB_8_WITHOUT_BANK().set_addr(0x%02x)" % self.addr

    def __str__(self):
        return "ADDR_GLB_8_WITHOUT_BANK(value=0x%x)" % self.value


class ADDR_GLB_64_WITHOUT_BANK(ADDR_GLB):

    def __init__(self, value: int = 0):
        super().__init__(True, False)
        self.value = int(value)

    def __repr__(self) -> str:
        return "ADDR_GLB_64_WITHOUT_BANK().set_addr(0x%02x)" % self.addr

    def __str__(self):
        return "ADDR_GLB_64_WITHOUT_BANK(value=0x%x)" % self.value


class ADDR_GLB_8_WITH_BANK(ADDR_GLB):

    def __init__(self, value: int = 0):
        super().__init__(False, True)
        self.value = int(value)

    def __repr__(self) -> str:
        return "ADDR_GLB_8_WITH_BANK().set_bank(0x%02x).set_addr(0x%02x)" % (
            self.bank, self.addr)

    def __str__(self):
        return "ADDR_GLB_8_WITH_BANK(value=0x%x)" % self.value


class ADDR_GLB_64_WITH_BANK(ADDR_GLB):

    def __init__(self, value: int = 0):
        super().__init__(True, True)
        self.value = int(value)

    def __repr__(self) -> str:
        return "ADDR_GLB_64_WITH_BANK().set_bank(0x%02x).set_addr(0x%02x)" % (
            self.bank, self.addr)

    def __str__(self):
        return "ADDR_GLB_64_WITH_BANK(value=0x%x)" % self.value


class UNION_ADDR():
    value: int

    def __init__(self,
                 value=None,
                 is_glb: bool = None,
                 addr: int = None,
                 bank: int = None):
        if value is not None:
            self.value = int(value)
            return
        self.value = 0
        self.glb = is_glb
        self.addr = addr
        if bank is not None:
            self.bank = bank

    def __int__(self):
        return self.value

    @staticmethod
    def ddr_flag() -> int:
        return 1 << 31

    @property
    def glb(self) -> bool:
        return self.value & (1 << 31) == 0

    @glb.setter
    def glb(self, value: bool):
        self.value = (self.value & 0x8FFFFFFF) | ((not value) << 31)

    @property
    def ddr(self) -> bool:
        return self.value & (1 << 31) != 0

    @ddr.setter
    def ddr(self, value: bool):
        self.value = (self.value & 0x8FFFFFFF) | (value << 31)

    @property
    def addr(self):
        if self.value & (1 << 31):
            return self.value & 0x8FFFFFFF
        else:
            return ADDR_GLB_8_WITH_BANK(self.value & 0xFFFFFF).addr

    @addr.setter
    def addr(self, value: int):
        if self.glb:
            new_addr = ADDR_GLB_8_WITH_BANK(self.value)
            new_addr.addr = value
            self.addr = self.addr & 0xFFFFFF | new_addr.value
        else:
            self.addr = value | (1 << 31)

    @property
    def bank(self) -> int:
        assert self.glb
        return ADDR_GLB_8_WITH_BANK(self.value).bank

    @bank.setter
    def bank(self, value: int):
        assert self.glb
        new_addr = ADDR_GLB_8_WITH_BANK(self.value)
        new_addr.bank = value
        self.addr = self.addr & 0xFFFFFF | new_addr.value

    def __str__(self) -> str:
        res = "UNION_ADDR(is_glb=%r, addr=0x%02x" % (self.glb, self.addr)
        if self.glb:
            res += ", bank=0x%02x)" % self.bank
        else:
            res += ')'

        return res

    def __repr__(self) -> str:
        return "UNION_ADDR(0x%02x)" % self.value


class BF24(int):
    pass


##################################
## auto generated structs


class MNCFG:

    value: int

    @property
    def s_2964729232734817346(self):
        return (self.value >> 0) & 0b11

    @s_2964729232734817346.setter
    def s_2964729232734817346(self, value: int):
        self.value = self.value & (~(0b11 << 0))
        self.value = self.value | ((value & (0b11)) << 0)

    @property
    def s_3784967002587739128(self):
        return (self.value >> 2) & 0b11

    @s_3784967002587739128.setter
    def s_3784967002587739128(self, value: int):
        self.value = self.value & (~(0b11 << 2))
        self.value = self.value | ((value & (0b11)) << 2)

    @property
    def s_2631191378607996507(self):
        return (self.value >> 4) & 0b11

    @s_2631191378607996507.setter
    def s_2631191378607996507(self, value: int):
        self.value = self.value & (~(0b11 << 4))
        self.value = self.value | ((value & (0b11)) << 4)

    @property
    def s_626945571255956340(self):
        return (self.value >> 6) & 0b11

    @s_626945571255956340.setter
    def s_626945571255956340(self, value: int):
        self.value = self.value & (~(0b11 << 6))
        self.value = self.value | ((value & (0b11)) << 6)

    @property
    def s_2736077837039385153(self):
        return (self.value >> 8) & 0b1

    @s_2736077837039385153.setter
    def s_2736077837039385153(self, value: int):
        self.value = self.value & (~(0b1 << 8))
        self.value = self.value | ((value & (0b1)) << 8)

    @property
    def s_459806009142642499(self):
        return (self.value >> 9) & 0b1

    @s_459806009142642499.setter
    def s_459806009142642499(self, value: int):
        self.value = self.value & (~(0b1 << 9))
        self.value = self.value | ((value & (0b1)) << 9)

    @property
    def s_6994553354653340116(self):
        return (self.value >> 10) & 0b1

    @s_6994553354653340116.setter
    def s_6994553354653340116(self, value: int):
        self.value = self.value & (~(0b1 << 10))
        self.value = self.value | ((value & (0b1)) << 10)

    @property
    def s_486948306752714979(self):
        return (self.value >> 11) & 0b1

    @s_486948306752714979.setter
    def s_486948306752714979(self, value: int):
        self.value = self.value & (~(0b1 << 11))
        self.value = self.value | ((value & (0b1)) << 11)

    @property
    def s_924874130317151342(self):
        return (self.value >> 12) & 0b1

    @s_924874130317151342.setter
    def s_924874130317151342(self, value: int):
        self.value = self.value & (~(0b1 << 12))
        self.value = self.value | ((value & (0b1)) << 12)

    @property
    def s_398152665207515301(self):
        return (self.value >> 13) & 0b1

    @s_398152665207515301.setter
    def s_398152665207515301(self, value: int):
        self.value = self.value & (~(0b1 << 13))
        self.value = self.value | ((value & (0b1)) << 13)

    @property
    def s_238263359635548616(self):
        return (self.value >> 14) & 0b11

    @s_238263359635548616.setter
    def s_238263359635548616(self, value: int):
        self.value = self.value & (~(0b11 << 14))
        self.value = self.value | ((value & (0b11)) << 14)

    @property
    def s_5252208633458543095(self):
        return (self.value >> 16) & 0b11

    @s_5252208633458543095.setter
    def s_5252208633458543095(self, value: int):
        self.value = self.value & (~(0b11 << 16))
        self.value = self.value | ((value & (0b11)) << 16)

    @property
    def s_3078320927331941066(self):
        return (self.value >> 18) & 0b11

    @s_3078320927331941066.setter
    def s_3078320927331941066(self, value: int):
        self.value = self.value & (~(0b11 << 18))
        self.value = self.value | ((value & (0b11)) << 18)

    @property
    def s_766110975335925518(self):
        return (self.value >> 20) & 0b1

    @s_766110975335925518.setter
    def s_766110975335925518(self, value: int):
        self.value = self.value & (~(0b1 << 20))
        self.value = self.value | ((value & (0b1)) << 20)

    @property
    def s_1134763790902225730(self):
        return (self.value >> 21) & 0b11

    @s_1134763790902225730.setter
    def s_1134763790902225730(self, value: int):
        self.value = self.value & (~(0b11 << 21))
        self.value = self.value | ((value & (0b11)) << 21)

    @property
    def s_3969879687980637557(self):
        return (self.value >> 23) & 0b11

    @s_3969879687980637557.setter
    def s_3969879687980637557(self, value: int):
        self.value = self.value & (~(0b11 << 23))
        self.value = self.value | ((value & (0b11)) << 23)

    @property
    def s_4214136596420842136(self):
        return (self.value >> 25) & 0b111

    @s_4214136596420842136.setter
    def s_4214136596420842136(self, value: int):
        self.value = self.value & (~(0b111 << 25))
        self.value = self.value | ((value & (0b111)) << 25)

    @property
    def s_4059078812785812405(self):
        return (self.value >> 28) & 0b111

    @s_4059078812785812405.setter
    def s_4059078812785812405(self, value: int):
        self.value = self.value & (~(0b111 << 28))
        self.value = self.value | ((value & (0b111)) << 28)

    def __str__(self) -> str:
        res = "MNCFG( "
        res += 's_2964729232734817346 = ' + str(
            self.s_2964729232734817346) + ','
        res += 's_3784967002587739128 = ' + str(
            self.s_3784967002587739128) + ','
        res += 's_2631191378607996507 = ' + str(
            self.s_2631191378607996507) + ','
        res += 's_626945571255956340 = ' + str(self.s_626945571255956340) + ','
        res += 's_2736077837039385153 = ' + str(
            self.s_2736077837039385153) + ','
        res += 's_459806009142642499 = ' + str(self.s_459806009142642499) + ','
        res += 's_6994553354653340116 = ' + str(
            self.s_6994553354653340116) + ','
        res += 's_486948306752714979 = ' + str(self.s_486948306752714979) + ','
        res += 's_924874130317151342 = ' + str(self.s_924874130317151342) + ','
        res += 's_398152665207515301 = ' + str(self.s_398152665207515301) + ','
        res += 's_238263359635548616 = ' + str(self.s_238263359635548616) + ','
        res += 's_5252208633458543095 = ' + str(
            self.s_5252208633458543095) + ','
        res += 's_3078320927331941066 = ' + str(
            self.s_3078320927331941066) + ','
        res += 's_766110975335925518 = ' + str(self.s_766110975335925518) + ','
        res += 's_1134763790902225730 = ' + str(
            self.s_1134763790902225730) + ','
        res += 's_3969879687980637557 = ' + str(
            self.s_3969879687980637557) + ','
        res += 's_4214136596420842136 = ' + str(
            self.s_4214136596420842136) + ','
        res += 's_4059078812785812405 = ' + str(
            self.s_4059078812785812405) + ','
        res += ')'
        return res

    def __repr__(self) -> str:
        res = "MNCFG("
        res += '\ts_2964729232734817346 = ' + str(
            self.s_2964729232734817346) + ','
        res += '\ts_3784967002587739128 = ' + str(
            self.s_3784967002587739128) + ','
        res += '\ts_2631191378607996507 = ' + str(
            self.s_2631191378607996507) + ','
        res += '\ts_626945571255956340 = ' + str(
            self.s_626945571255956340) + ','
        res += '\ts_2736077837039385153 = ' + str(
            self.s_2736077837039385153) + ','
        res += '\ts_459806009142642499 = ' + str(
            self.s_459806009142642499) + ','
        res += '\ts_6994553354653340116 = ' + str(
            self.s_6994553354653340116) + ','
        res += '\ts_486948306752714979 = ' + str(
            self.s_486948306752714979) + ','
        res += '\ts_924874130317151342 = ' + str(
            self.s_924874130317151342) + ','
        res += '\ts_398152665207515301 = ' + str(
            self.s_398152665207515301) + ','
        res += '\ts_238263359635548616 = ' + str(
            self.s_238263359635548616) + ','
        res += '\ts_5252208633458543095 = ' + str(
            self.s_5252208633458543095) + ','
        res += '\ts_3078320927331941066 = ' + str(
            self.s_3078320927331941066) + ','
        res += '\ts_766110975335925518 = ' + str(
            self.s_766110975335925518) + ','
        res += '\ts_1134763790902225730 = ' + str(
            self.s_1134763790902225730) + ','
        res += '\ts_3969879687980637557 = ' + str(
            self.s_3969879687980637557) + ','
        res += '\ts_4214136596420842136 = ' + str(
            self.s_4214136596420842136) + ','
        res += '\ts_4059078812785812405 = ' + str(
            self.s_4059078812785812405) + ','
        res += ')'
        return str(self)

    def __init__(
        self,
        value=None,
        s_2964729232734817346: int = None,
        s_3784967002587739128: int = None,
        s_2631191378607996507: int = None,
        s_626945571255956340: int = None,
        s_2736077837039385153: int = None,
        s_459806009142642499: int = None,
        s_6994553354653340116: int = None,
        s_486948306752714979: int = None,
        s_924874130317151342: int = None,
        s_398152665207515301: int = None,
        s_238263359635548616: int = None,
        s_5252208633458543095: int = None,
        s_3078320927331941066: int = None,
        s_766110975335925518: int = None,
        s_1134763790902225730: int = None,
        s_3969879687980637557: int = None,
        s_4214136596420842136: int = None,
        s_4059078812785812405: int = None,
    ):
        self.value = 0
        if value is not None:
            if isinstance(value, int):
                self.value = value
            elif isinstance(value, MNCFG):
                self.s_2964729232734817346 = value.s_2964729232734817346
                self.s_3784967002587739128 = value.s_3784967002587739128
                self.s_2631191378607996507 = value.s_2631191378607996507
                self.s_626945571255956340 = value.s_626945571255956340
                self.s_2736077837039385153 = value.s_2736077837039385153
                self.s_459806009142642499 = value.s_459806009142642499
                self.s_6994553354653340116 = value.s_6994553354653340116
                self.s_486948306752714979 = value.s_486948306752714979
                self.s_924874130317151342 = value.s_924874130317151342
                self.s_398152665207515301 = value.s_398152665207515301
                self.s_238263359635548616 = value.s_238263359635548616
                self.s_5252208633458543095 = value.s_5252208633458543095
                self.s_3078320927331941066 = value.s_3078320927331941066
                self.s_766110975335925518 = value.s_766110975335925518
                self.s_1134763790902225730 = value.s_1134763790902225730
                self.s_3969879687980637557 = value.s_3969879687980637557
                self.s_4214136596420842136 = value.s_4214136596420842136
                self.s_4059078812785812405 = value.s_4059078812785812405
        else:
            if s_2964729232734817346:
                self.s_2964729232734817346 = s_2964729232734817346
            if s_3784967002587739128:
                self.s_3784967002587739128 = s_3784967002587739128
            if s_2631191378607996507:
                self.s_2631191378607996507 = s_2631191378607996507
            if s_626945571255956340:
                self.s_626945571255956340 = s_626945571255956340
            if s_2736077837039385153:
                self.s_2736077837039385153 = s_2736077837039385153
            if s_459806009142642499:
                self.s_459806009142642499 = s_459806009142642499
            if s_6994553354653340116:
                self.s_6994553354653340116 = s_6994553354653340116
            if s_486948306752714979:
                self.s_486948306752714979 = s_486948306752714979
            if s_924874130317151342:
                self.s_924874130317151342 = s_924874130317151342
            if s_398152665207515301:
                self.s_398152665207515301 = s_398152665207515301
            if s_238263359635548616:
                self.s_238263359635548616 = s_238263359635548616
            if s_5252208633458543095:
                self.s_5252208633458543095 = s_5252208633458543095
            if s_3078320927331941066:
                self.s_3078320927331941066 = s_3078320927331941066
            if s_766110975335925518:
                self.s_766110975335925518 = s_766110975335925518
            if s_1134763790902225730:
                self.s_1134763790902225730 = s_1134763790902225730
            if s_3969879687980637557:
                self.s_3969879687980637557 = s_3969879687980637557
            if s_4214136596420842136:
                self.s_4214136596420842136 = s_4214136596420842136
            if s_4059078812785812405:
                self.s_4059078812785812405 = s_4059078812785812405

    pass

    def __int__(self):
        return self.value


class QARG:

    value: int

    @property
    def s_1582559245318645089(self):
        return (self.value >> 0) & 0b1111111111111111

    @s_1582559245318645089.setter
    def s_1582559245318645089(self, value: int):
        self.value = self.value & (~(0b1111111111111111 << 0))
        self.value = self.value | ((value & (0b1111111111111111)) << 0)

    @property
    def s_7146229244009115437(self):
        return (self.value >> 16) & 0b11111111

    @s_7146229244009115437.setter
    def s_7146229244009115437(self, value: int):
        self.value = self.value & (~(0b11111111 << 16))
        self.value = self.value | ((value & (0b11111111)) << 16)

    @property
    def s_4927171469365949165(self):
        return (self.value >> 24) & 0b11111111

    @s_4927171469365949165.setter
    def s_4927171469365949165(self, value: int):
        self.value = self.value & (~(0b11111111 << 24))
        self.value = self.value | ((value & (0b11111111)) << 24)

    def __str__(self) -> str:
        res = "QARG( "
        res += 's_1582559245318645089 = ' + str(
            self.s_1582559245318645089) + ','
        res += 's_7146229244009115437 = ' + str(
            self.s_7146229244009115437) + ','
        res += 's_4927171469365949165 = ' + str(
            self.s_4927171469365949165) + ','
        res += ')'
        return res

    def __repr__(self) -> str:
        res = "QARG("
        res += '\ts_1582559245318645089 = ' + str(
            self.s_1582559245318645089) + ','
        res += '\ts_7146229244009115437 = ' + str(
            self.s_7146229244009115437) + ','
        res += '\ts_4927171469365949165 = ' + str(
            self.s_4927171469365949165) + ','
        res += ')'
        return str(self)

    def __init__(
        self,
        value=None,
        s_1582559245318645089: int = None,
        s_7146229244009115437: int = None,
        s_4927171469365949165: int = None,
    ):
        self.value = 0
        if value is not None:
            if isinstance(value, int):
                self.value = value
            elif isinstance(value, QARG):
                self.s_1582559245318645089 = value.s_1582559245318645089
                self.s_7146229244009115437 = value.s_7146229244009115437
                self.s_4927171469365949165 = value.s_4927171469365949165
        else:
            if s_1582559245318645089:
                self.s_1582559245318645089 = s_1582559245318645089
            if s_7146229244009115437:
                self.s_7146229244009115437 = s_7146229244009115437
            if s_4927171469365949165:
                self.s_4927171469365949165 = s_4927171469365949165

    pass

    def __int__(self):
        return self.value


class CCRCLR:

    value: int

    @property
    def s_1374817876057092918(self):
        return (self.value >> 0) & 0b1

    @s_1374817876057092918.setter
    def s_1374817876057092918(self, value: int):
        self.value = self.value & (~(0b1 << 0))
        self.value = self.value | ((value & (0b1)) << 0)

    @property
    def s_5085793024541575481(self):
        return (self.value >> 1) & 0b111111

    @s_5085793024541575481.setter
    def s_5085793024541575481(self, value: int):
        self.value = self.value & (~(0b111111 << 1))
        self.value = self.value | ((value & (0b111111)) << 1)

    @property
    def s_1748548688350378073(self):
        return (self.value >> 7) & 0b1

    @s_1748548688350378073.setter
    def s_1748548688350378073(self, value: int):
        self.value = self.value & (~(0b1 << 7))
        self.value = self.value | ((value & (0b1)) << 7)

    def __str__(self) -> str:
        res = "CCRCLR( "
        res += 's_1374817876057092918 = ' + str(
            self.s_1374817876057092918) + ','
        res += 's_5085793024541575481 = ' + str(
            self.s_5085793024541575481) + ','
        res += 's_1748548688350378073 = ' + str(
            self.s_1748548688350378073) + ','
        res += ')'
        return res

    def __repr__(self) -> str:
        res = "CCRCLR("
        res += '\ts_1374817876057092918 = ' + str(
            self.s_1374817876057092918) + ','
        res += '\ts_5085793024541575481 = ' + str(
            self.s_5085793024541575481) + ','
        res += '\ts_1748548688350378073 = ' + str(
            self.s_1748548688350378073) + ','
        res += ')'
        return str(self)

    def __init__(
        self,
        value=None,
        s_1374817876057092918: int = None,
        s_5085793024541575481: int = None,
        s_1748548688350378073: int = None,
    ):
        self.value = 0
        if value is not None:
            if isinstance(value, int):
                self.value = value
            elif isinstance(value, CCRCLR):
                self.s_1374817876057092918 = value.s_1374817876057092918
                self.s_5085793024541575481 = value.s_5085793024541575481
                self.s_1748548688350378073 = value.s_1748548688350378073
        else:
            if s_1374817876057092918:
                self.s_1374817876057092918 = s_1374817876057092918
            if s_5085793024541575481:
                self.s_5085793024541575481 = s_5085793024541575481
            if s_1748548688350378073:
                self.s_1748548688350378073 = s_1748548688350378073

    pass

    def __int__(self):
        return self.value


class STRIDE_GLB:

    value: int

    @property
    def s_2747657756698496122(self):
        return (self.value >> 0) & 0b111111111111111111111

    @s_2747657756698496122.setter
    def s_2747657756698496122(self, value: int):
        self.value = self.value & (~(0b111111111111111111111 << 0))
        self.value = self.value | ((value & (0b111111111111111111111)) << 0)

    @property
    def s_7119413225195592970(self):
        return (self.value >> 21) & 0b111111111111111111111

    @s_7119413225195592970.setter
    def s_7119413225195592970(self, value: int):
        self.value = self.value & (~(0b111111111111111111111 << 21))
        self.value = self.value | ((value & (0b111111111111111111111)) << 21)

    @property
    def s_6802197150470736984(self):
        return (self.value >> 42) & 0b111111111111111111111

    @s_6802197150470736984.setter
    def s_6802197150470736984(self, value: int):
        self.value = self.value & (~(0b111111111111111111111 << 42))
        self.value = self.value | ((value & (0b111111111111111111111)) << 42)

    def __str__(self) -> str:
        res = "STRIDE_GLB( "
        res += 's_2747657756698496122 = ' + str(
            self.s_2747657756698496122) + ','
        res += 's_7119413225195592970 = ' + str(
            self.s_7119413225195592970) + ','
        res += 's_6802197150470736984 = ' + str(
            self.s_6802197150470736984) + ','
        res += ')'
        return res

    def __repr__(self) -> str:
        res = "STRIDE_GLB("
        res += '\ts_2747657756698496122 = ' + str(
            self.s_2747657756698496122) + ','
        res += '\ts_7119413225195592970 = ' + str(
            self.s_7119413225195592970) + ','
        res += '\ts_6802197150470736984 = ' + str(
            self.s_6802197150470736984) + ','
        res += ')'
        return str(self)

    def __init__(
        self,
        value=None,
        s_2747657756698496122: int = None,
        s_7119413225195592970: int = None,
        s_6802197150470736984: int = None,
    ):
        self.value = 0
        if value is not None:
            if isinstance(value, int):
                self.value = value
            elif isinstance(value, STRIDE_GLB):
                self.s_2747657756698496122 = value.s_2747657756698496122
                self.s_7119413225195592970 = value.s_7119413225195592970
                self.s_6802197150470736984 = value.s_6802197150470736984
        else:
            if s_2747657756698496122:
                self.s_2747657756698496122 = s_2747657756698496122
            if s_7119413225195592970:
                self.s_7119413225195592970 = s_7119413225195592970
            if s_6802197150470736984:
                self.s_6802197150470736984 = s_6802197150470736984

    pass

    def __int__(self):
        return self.value


class CCRSET:

    value: int

    @property
    def s_4726129186757708156(self):
        return (self.value >> 0) & 0b1

    @s_4726129186757708156.setter
    def s_4726129186757708156(self, value: int):
        self.value = self.value & (~(0b1 << 0))
        self.value = self.value | ((value & (0b1)) << 0)

    @property
    def s_5085793024541575481(self):
        return (self.value >> 1) & 0b111111

    @s_5085793024541575481.setter
    def s_5085793024541575481(self, value: int):
        self.value = self.value & (~(0b111111 << 1))
        self.value = self.value | ((value & (0b111111)) << 1)

    @property
    def s_8038091067621949879(self):
        return (self.value >> 7) & 0b1111

    @s_8038091067621949879.setter
    def s_8038091067621949879(self, value: int):
        self.value = self.value & (~(0b1111 << 7))
        self.value = self.value | ((value & (0b1111)) << 7)

    def __str__(self) -> str:
        res = "CCRSET( "
        res += 's_4726129186757708156 = ' + str(
            self.s_4726129186757708156) + ','
        res += 's_5085793024541575481 = ' + str(
            self.s_5085793024541575481) + ','
        res += 's_8038091067621949879 = ' + str(
            self.s_8038091067621949879) + ','
        res += ')'
        return res

    def __repr__(self) -> str:
        res = "CCRSET("
        res += '\ts_4726129186757708156 = ' + str(
            self.s_4726129186757708156) + ','
        res += '\ts_5085793024541575481 = ' + str(
            self.s_5085793024541575481) + ','
        res += '\ts_8038091067621949879 = ' + str(
            self.s_8038091067621949879) + ','
        res += ')'
        return str(self)

    def __init__(
        self,
        value=None,
        s_4726129186757708156: int = None,
        s_5085793024541575481: int = None,
        s_8038091067621949879: int = None,
    ):
        self.value = 0
        if value is not None:
            if isinstance(value, int):
                self.value = value
            elif isinstance(value, CCRSET):
                self.s_4726129186757708156 = value.s_4726129186757708156
                self.s_5085793024541575481 = value.s_5085793024541575481
                self.s_8038091067621949879 = value.s_8038091067621949879
        else:
            if s_4726129186757708156:
                self.s_4726129186757708156 = s_4726129186757708156
            if s_5085793024541575481:
                self.s_5085793024541575481 = s_5085793024541575481
            if s_8038091067621949879:
                self.s_8038091067621949879 = s_8038091067621949879

    pass

    def __int__(self):
        return self.value


##################################
## auto generated enums
class MFU_CROP_ALIGN(Enum):

    MFU_CROP_ALIGN_EV_8020117326212680870 = 0x0

    MFU_CROP_ALIGN_EV_479959117184035876 = 0x1

    MFU_CROP_ALIGN_EV_7999968760708582066 = 0x2

    def __int__(self):
        return self.value


class MFU_REDUCE_DIM(Enum):

    MFU_REDUCE_DIM_EV_5160612990728314706 = 0x0

    MFU_REDUCE_DIM_EV_5521155195140420950 = 0x1

    MFU_REDUCE_DIM_EV_2232069558367812092 = 0x2

    MFU_REDUCE_DIM_EV_8981332216981304004 = 0x3

    def __int__(self):
        return self.value


class MFU_PDP_OP(Enum):

    MFU_PDP_OP_EV_592609557505209875 = 0x1

    MFU_PDP_OP_EV_735611942548257723 = 0x0

    MFU_PDP_OP_EV_6352330561201538803 = 0x2

    MFU_PDP_OP_EV_4892129865498131768 = 0x3

    def __int__(self):
        return self.value


class MFU_REDUCE_OP(Enum):

    MFU_REDUCE_OP_EV_735611942548257723 = 0x0

    MFU_REDUCE_OP_EV_592609557505209875 = 0x1

    MFU_REDUCE_OP_EV_8697260873104641532 = 0x2

    MFU_REDUCE_OP_EV_1531524865243936302 = 0x3

    MFU_REDUCE_OP_EV_6898495038438589832 = 0x4

    def __int__(self):
        return self.value


class MFU_CROP_RESIZE(Enum):

    MFU_CROP_RESIZE_EV_7608549848760985318 = 0x0

    MFU_CROP_RESIZE_EV_2127141166558419689 = 0x1

    def __int__(self):
        return self.value


class COMPRESSED(Enum):

    COMPRESSED_EV_5236511592690819359 = 0x0

    COMPRESSED_EV_8160868962009034665 = 0x1

    def __int__(self):
        return self.value


class QUAN_TYPE(Enum):

    QUAN_TYPE_EV_3071692942176476695 = 0x0

    QUAN_TYPE_EV_6279706699589965600 = 0x1

    def __int__(self):
        return self.value


class PRECISION(Enum):

    PRECISION_EV_5454463369874334077 = 0x0

    PRECISION_EV_1211632620008582644 = 0x1

    PRECISION_EV_7934974854498115910 = 0x2

    def __int__(self):
        return self.value


class MMU_CONF_WIDTH(Enum):

    MMU_CONF_WIDTH_EV_1 = 0x0

    MMU_CONF_WIDTH_EV_2 = 0x1

    MMU_CONF_WIDTH_EV_4 = 0x2

    MMU_CONF_WIDTH_EV_8 = 0x3

    def __int__(self):
        return self.value


class MFU_MN_OP(Enum):

    MFU_MN_OP_EV_6622293485249721470 = 0x0

    MFU_MN_OP_EV_7566276794240323573 = 0x1

    MFU_MN_OP_EV_2813029168831662022 = 0x2

    MFU_MN_OP_EV_1305277825823933909 = 0x3

    MFU_MN_OP_EV_7392438048383640188 = 0x4

    MFU_MN_OP_EV_3315136436991357796 = 0x5

    MFU_MN_OP_EV_7090139616952759397 = 0x6

    MFU_MN_OP_EV_6036731965487374061 = 0x7

    MFU_MN_OP_EV_5337694862214031301 = 0x8

    MFU_MN_OP_EV_5431039917951081015 = 0x9

    MFU_MN_OP_EV_2215364621533182461 = 0xa

    MFU_MN_OP_EV_7475737086447188411 = 0xb

    MFU_MN_OP_EV_3148033175416006587 = 0xc

    MFU_MN_OP_EV_7951594608521869513 = 0xd

    MFU_MN_OP_EV_2694741306110262927 = 0xe

    MFU_MN_OP_EV_6729989405168212429 = 0xf

    MFU_MN_OP_EV_4471345555019198640 = 0x10

    MFU_MN_OP_EV_1249420413945110379 = 0x11

    MFU_MN_OP_EV_7538782904175654026 = 0x12

    MFU_MN_OP_EV_7628262002576754229 = 0x13

    MFU_MN_OP_EV_1268981042392956554 = 0x14

    MFU_MN_OP_EV_6752888727492488062 = 0x15

    MFU_MN_OP_EV_6450813677640145607 = 0x16

    MFU_MN_OP_EV_5635907193489745983 = 0x17

    MFU_MN_OP_EV_5568194703282893645 = 0x18

    MFU_MN_OP_EV_7166539770309708351 = 0x19

    MFU_MN_OP_EV_3825803578007987832 = 0x1a

    MFU_MN_OP_EV_2041966296396375781 = 0x1b

    MFU_MN_OP_EV_761273868355891943 = 0x1c

    MFU_MN_OP_EV_5397818987121026551 = 0x1d

    MFU_MN_OP_EV_1249395507916995686 = 0x1e

    def __int__(self):
        return self.value


class MFU_TRANS_PERMUTE(Enum):

    MFU_TRANS_PERMUTE_EV_8981332216981304004 = 0x0

    MFU_TRANS_PERMUTE_EV_5645261511825289758 = 0x1

    MFU_TRANS_PERMUTE_EV_2281902186686404109 = 0x2

    MFU_TRANS_PERMUTE_EV_4313963510076719982 = 0x3

    MFU_TRANS_PERMUTE_EV_2461314065642081873 = 0x4

    MFU_TRANS_PERMUTE_EV_4657840826849733890 = 0x5

    MFU_TRANS_PERMUTE_EV_6730996868389108065 = 0x6

    MFU_TRANS_PERMUTE_EV_8583101013427625110 = 0x7

    MFU_TRANS_PERMUTE_EV_6781083456347313583 = 0x8

    MFU_TRANS_PERMUTE_EV_4709942040471818327 = 0x9

    MFU_TRANS_PERMUTE_EV_1937918449685041880 = 0xa

    MFU_TRANS_PERMUTE_EV_7626323780072559023 = 0xb

    MFU_TRANS_PERMUTE_EV_4626192377878894587 = 0xc

    MFU_TRANS_PERMUTE_EV_5256561681996076887 = 0xd

    MFU_TRANS_PERMUTE_EV_1557191823128663943 = 0xe

    MFU_TRANS_PERMUTE_EV_7572765764930436655 = 0xf

    MFU_TRANS_PERMUTE_EV_3382374794542279904 = 0x10

    MFU_TRANS_PERMUTE_EV_5185214553084584554 = 0x11

    MFU_TRANS_PERMUTE_EV_8779460261207081631 = 0x12

    MFU_TRANS_PERMUTE_EV_814742013828334886 = 0x13

    MFU_TRANS_PERMUTE_EV_8073214941780710639 = 0x14

    MFU_TRANS_PERMUTE_EV_3155566905680769545 = 0x15

    MFU_TRANS_PERMUTE_EV_3400608604143523417 = 0x16

    MFU_TRANS_PERMUTE_EV_8129255272664039236 = 0x17

    def __int__(self):
        return self.value


class TCU_MODE(Enum):

    TCU_MODE_EV_9155057194773964157 = 0x0

    TCU_MODE_EV_1416362977654493841 = 0x1

    TCU_MODE_EV_3794431211175078165 = 0x2

    TCU_MODE_EV_6722970019601813678 = 0x3

    def __int__(self):
        return self.value


class QUAN_SIGNED(Enum):

    QUAN_SIGNED_EV_2780359682732038963 = 0x0

    QUAN_SIGNED_EV_8813027230969607599 = 0x1

    def __int__(self):
        return self.value


class BROADCAST(Enum):

    BROADCAST_EV_1335548620187016595 = 0x0

    BROADCAST_EV_3000779319504675285 = 0x1

    def __int__(self):
        return self.value


class SPARSIFIED(Enum):

    SPARSIFIED_EV_8650383105711410522 = 0x0

    SPARSIFIED_EV_2046808399293827619 = 0x1

    def __int__(self):
        return self.value


class MFU_MN_PORTIN(Enum):

    MFU_MN_PORTIN_EV_2898721940358709965 = 0x0

    MFU_MN_PORTIN_EV_513778432285666813 = 0x1

    MFU_MN_PORTIN_EV_1811544539644467852 = 0x2

    MFU_MN_PORTIN_EV_5233752000623382252 = 0x3

    MFU_MN_PORTIN_EV_2699469598001748917 = 0x4

    MFU_MN_PORTIN_EV_5522125988120593182 = 0x5

    MFU_MN_PORTIN_EV_3979205303831078058 = 0x6

    MFU_MN_PORTIN_EV_162893306773436746 = 0x7

    MFU_MN_PORTIN_EV_8267938858859484090 = 0x8

    MFU_MN_PORTIN_EV_5963298331071166225 = 0x9

    MFU_MN_PORTIN_EV_3283655329219244013 = 0xa

    MFU_MN_PORTIN_EV_4818594583184613910 = 0xb

    MFU_MN_PORTIN_EV_4595298667720459214 = 0xc

    MFU_MN_PORTIN_EV_7592686134536536323 = 0xd

    MFU_MN_PORTIN_EV_5888038688442470558 = 0xe

    MFU_MN_PORTIN_EV_1964467220919210851 = 0xf

    MFU_MN_PORTIN_EV_1901523637126839365 = 0x10

    MFU_MN_PORTIN_EV_2866255204895793247 = 0x11

    MFU_MN_PORTIN_EV_627869992386291710 = 0x12

    MFU_MN_PORTIN_EV_7558959592645579123 = 0x13

    MFU_MN_PORTIN_EV_8797466131014360670 = 0x14

    MFU_MN_PORTIN_EV_2302437988002225505 = 0x15

    MFU_MN_PORTIN_EV_6707964778406420745 = 0x16

    MFU_MN_PORTIN_EV_1974921128489510036 = 0x17

    MFU_MN_PORTIN_EV_8727000878094284137 = 0x18

    MFU_MN_PORTIN_EV_3318387536984992082 = 0x19

    MFU_MN_PORTIN_EV_8338456426195563065 = 0x1a

    MFU_MN_PORTIN_EV_1087239042952831214 = 0x1b

    MFU_MN_PORTIN_EV_1245616756383641495 = 0x1c

    MFU_MN_PORTIN_EV_7874133826069032087 = 0x1d

    MFU_MN_PORTIN_EV_6490485170613801903 = 0x1e

    MFU_MN_PORTIN_EV_7094550568757388289 = 0x1f

    MFU_MN_PORTIN_EV_5676311761514233773 = 0x20

    MFU_MN_PORTIN_EV_9104573644466761519 = 0x21

    MFU_MN_PORTIN_EV_5153984532988777971 = 0x22

    MFU_MN_PORTIN_EV_4340975839513126126 = 0x23

    MFU_MN_PORTIN_EV_7498009403962098592 = 0x24

    MFU_MN_PORTIN_EV_489833323810591526 = 0x25

    def __int__(self):
        return self.value


class MFU_MN_PORTOUT(Enum):

    MFU_MN_PORTOUT_EV_2898721940358709965 = 0x0

    MFU_MN_PORTOUT_EV_7898938705131623749 = 0x1

    MFU_MN_PORTOUT_EV_3995341855104245382 = 0x2

    MFU_MN_PORTOUT_EV_2268095463929474955 = 0x3

    MFU_MN_PORTOUT_EV_6387419815495568078 = 0x4

    MFU_MN_PORTOUT_EV_4004431816360206406 = 0x5

    MFU_MN_PORTOUT_EV_5596464065239254683 = 0x6

    MFU_MN_PORTOUT_EV_4927716699040792521 = 0x7

    MFU_MN_PORTOUT_EV_6264300983398299253 = 0x8

    MFU_MN_PORTOUT_EV_7295665352974468100 = 0x9

    MFU_MN_PORTOUT_EV_5263823472704949326 = 0xa

    MFU_MN_PORTOUT_EV_3268038709448010983 = 0xb

    MFU_MN_PORTOUT_EV_62742329097144405 = 0xc

    MFU_MN_PORTOUT_EV_7076583550253641103 = 0xd

    MFU_MN_PORTOUT_EV_1320974831723486899 = 0xe

    MFU_MN_PORTOUT_EV_2651518189268085927 = 0xf

    MFU_MN_PORTOUT_EV_4935052267669527658 = 0x10

    MFU_MN_PORTOUT_EV_527790612825583299 = 0x11

    MFU_MN_PORTOUT_EV_1550748740801939877 = 0x12

    MFU_MN_PORTOUT_EV_4819196648789177867 = 0x13

    MFU_MN_PORTOUT_EV_8758541369253966412 = 0x14

    MFU_MN_PORTOUT_EV_6334766990151572184 = 0x15

    MFU_MN_PORTOUT_EV_6952959116698996564 = 0x16

    MFU_MN_PORTOUT_EV_4625809560484933494 = 0x17

    MFU_MN_PORTOUT_EV_2663153453538865891 = 0x18

    MFU_MN_PORTOUT_EV_3340691047976680373 = 0x19

    MFU_MN_PORTOUT_EV_2349416763159088999 = 0x1a

    MFU_MN_PORTOUT_EV_8751179784572183834 = 0x1b

    MFU_MN_PORTOUT_EV_3981947495312575043 = 0x1c

    MFU_MN_PORTOUT_EV_1113953178920247433 = 0x1d

    MFU_MN_PORTOUT_EV_3845809167795234212 = 0x1e

    MFU_MN_PORTOUT_EV_5455370935651255486 = 0x1f

    MFU_MN_PORTOUT_EV_3553020416195645168 = 0x20

    MFU_MN_PORTOUT_EV_3491720287682176967 = 0x21

    MFU_MN_PORTOUT_EV_7623582717574480668 = 0x22

    MFU_MN_PORTOUT_EV_3363885953231210215 = 0x23

    MFU_MN_PORTOUT_EV_277394929094750302 = 0x24

    MFU_MN_PORTOUT_EV_3736858657437761182 = 0x25

    MFU_MN_PORTOUT_EV_5375658941104271894 = 0x26

    MFU_MN_PORTOUT_EV_8043643152678609136 = 0x27

    MFU_MN_PORTOUT_EV_6456965168586493274 = 0x28

    MFU_MN_PORTOUT_EV_6290935645352351864 = 0x29

    MFU_MN_PORTOUT_EV_4949872236695873069 = 0x2a

    MFU_MN_PORTOUT_EV_1817212964311931731 = 0x2b

    MFU_MN_PORTOUT_EV_4109651311163243558 = 0x2c

    def __int__(self):
        return self.value


class OPCODE(Enum):

    OPCODE_EV_6674109482354074040 = 0x0

    OPCODE_EV_304026372243538007 = 0x1

    OPCODE_EV_4723717955423805745 = 0x2

    OPCODE_EV_328345304491746530 = 0x3

    OPCODE_EV_8790047992392043228 = 0x4

    OPCODE_EV_7155768076259033706 = 0x5

    OPCODE_EV_4539906387927636499 = 0x8

    OPCODE_EV_4968684677827927616 = 0x10

    OPCODE_EV_6647669131517538538 = 0x11

    OPCODE_EV_6703668108300758238 = 0x12

    OPCODE_EV_5869363465604696689 = 0x13

    OPCODE_EV_9152920230794971550 = 0x14

    OPCODE_EV_7204637145564182256 = 0x15

    OPCODE_EV_2089276022054688120 = 0x20

    OPCODE_EV_2841594760846416640 = 0x21

    OPCODE_EV_3414519735293012969 = 0x22

    OPCODE_EV_4825624964056672963 = 0x23

    OPCODE_EV_3246495767012874974 = 0x24

    OPCODE_EV_8339684182387014894 = 0x25

    OPCODE_EV_6868657659093990379 = 0x41

    OPCODE_EV_8430774666881311866 = 0x42

    OPCODE_EV_6471126574510039166 = 0x43

    OPCODE_EV_6369672458787877517 = 0x44

    OPCODE_EV_7025294518658670577 = 0x45

    OPCODE_EV_6731377247628139860 = 0x46

    OPCODE_EV_5088819369833811485 = 0x47

    OPCODE_EV_7758253786169375348 = 0x48

    OPCODE_EV_8336797519624639034 = 0x49

    OPCODE_EV_2090902360472978351 = 0x4a

    OPCODE_EV_4164694345981782964 = 0x4b

    OPCODE_EV_4473276217691097372 = 0x4c

    OPCODE_EV_4137136459015411447 = 0x4d

    OPCODE_EV_4473749037637649123 = 0x4e

    OPCODE_EV_214212455253550760 = 0x4f

    OPCODE_EV_7571105850837497638 = 0x81

    OPCODE_EV_4966324269173843223 = 0x82

    OPCODE_EV_6096737859014398957 = 0x83

    OPCODE_EV_4266661972367639294 = 0x84

    OPCODE_EV_1712250146653531835 = 0x85

    OPCODE_EV_447177514076795622 = 0x86

    OPCODE_EV_2656964308044352142 = 0x87

    OPCODE_EV_7317298242942939054 = 0x88

    OPCODE_EV_4940390838445604897 = 0x89

    OPCODE_EV_7071148236208088088 = 0x8a

    OPCODE_EV_3215644467781021096 = 0x8b

    OPCODE_EV_4300588898699658039 = 0x8c

    OPCODE_EV_4573608092199809765 = 0x8d

    OPCODE_EV_3562245241250454416 = 0x8e

    OPCODE_EV_7361852897854452313 = 0x8f

    OPCODE_EV_2506286750019430415 = 0x90

    OPCODE_EV_245645227484541732 = 0x91

    def __int__(self):
        return self.value


class STORE_ORDER(Enum):

    STORE_ORDER_EV_8981332216981304004 = 0x0

    STORE_ORDER_EV_2281902186686404109 = 0x1

    def __int__(self):
        return self.value


class LOAD_ORDER(Enum):

    LOAD_ORDER_EV_8981332216981304004 = 0x0

    LOAD_ORDER_EV_6578088711676068457 = 0x1

    LOAD_ORDER_EV_2843838740657316125 = 0x2

    LOAD_ORDER_EV_447282046145446131 = 0x3

    LOAD_ORDER_EV_8791788928435158905 = 0x4

    LOAD_ORDER_EV_7443896215168224893 = 0x5

    LOAD_ORDER_EV_1890543803873349694 = 0x6

    LOAD_ORDER_EV_6599958810081011861 = 0x7

    LOAD_ORDER_EV_1843682403903277751 = 0x8

    LOAD_ORDER_EV_4896548880282225780 = 0x9

    LOAD_ORDER_EV_3717178866180522894 = 0xa

    LOAD_ORDER_EV_8036481329891141950 = 0xb

    LOAD_ORDER_EV_8206123993663862941 = 0xc

    LOAD_ORDER_EV_8221300725587479488 = 0xd

    LOAD_ORDER_EV_6042462808261736209 = 0xe

    LOAD_ORDER_EV_1911629336480606048 = 0xf

    LOAD_ORDER_EV_9129332208924365113 = 0x10

    LOAD_ORDER_EV_7870493510354931956 = 0x11

    LOAD_ORDER_EV_4545601307871831942 = 0x12

    def __int__(self):
        return self.value


class ALIGNED(Enum):

    ALIGNED_EV_8650383105711410522 = 0x0

    ALIGNED_EV_1837076777799932414 = 0x1

    def __int__(self):
        return self.value


class PRECISION_DDR(Enum):

    PRECISION_DDR_EV_5454463369874334077 = 0x0

    PRECISION_DDR_EV_1211632620008582644 = 0x1

    PRECISION_DDR_EV_7934974854498115910 = 0x2

    PRECISION_DDR_EV_2227045067087856724 = 0x3

    PRECISION_DDR_EV_2829558833882753521 = 0x4

    def __int__(self):
        return self.value


##################################
## auto generated instructions

OldProperty = property
property = HookProperty


class inst_i_6674109482354074040(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore

    def __init__(self, value: Union[bytes, str] = None, hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        self.opcode = OPCODE(0)

    def fields(self,):
        return self

    def pack(self) -> bytes:
        return self.cf.pack(int(self.f_2886468954866643279),)[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 1
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x0
        (self.f_2886468954866643279,) = res

    def __repr__(self):
        return 'inst_i_6674109482354074040(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_6674109482354074040().fields(\n'
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 1

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)


class inst_i_304026372243538007(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_1177787925382175493: [REG, 5]  # type: ignore
    __f_7714181516199238740: [datatype.uint64, 64]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[REG, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(3)

        self.__f_7714181516199238740 = int(0)
        cf_str += '>u64'
        self.__f_1177787925382175493 = REG(0)
        cf_str += '>u5'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(1)

    def fields(
        self,
        f_1177787925382175493: REG = None,
        f_7714181516199238740: int = None,
    ):
        if f_1177787925382175493:
            self.f_1177787925382175493 = f_1177787925382175493
        if f_7714181516199238740:
            self.f_7714181516199238740 = f_7714181516199238740
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_7714181516199238740),
            int(self.f_1177787925382175493),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 10
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x1
        (
            self.f_7714181516199238740,
            self.f_1177787925382175493,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_304026372243538007(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_304026372243538007().fields(\n'
        res += '\tf_1177787925382175493 = %s ,\n' % str(
            self.f_1177787925382175493)
        res += '\tf_7714181516199238740 = %s ,\n' % str(
            self.f_7714181516199238740)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 10

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_1177787925382175493(self):
        return self.__f_1177787925382175493

    def __set_f_1177787925382175493(self, value):

        assert (isinstance(value, (int, REG)))
        self.__f_1177787925382175493 = value if isinstance(value,
                                                           REG) else REG(value)

    def __get_f_7714181516199238740(self):
        return self.__f_7714181516199238740

    def __set_f_7714181516199238740(self, value):
        assert int(value) < 2**64

        assert int(value) >= 0

        self.__f_7714181516199238740 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_1177787925382175493 = property(__get_f_1177787925382175493,
                                     __set_f_1177787925382175493)
    f_7714181516199238740 = property(__get_f_7714181516199238740,
                                     __set_f_7714181516199238740)


class inst_i_4723717955423805745(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_972799269597490421: [datatype.uint32, 32]  # type: ignore
    __f_7839095738514289283: [datatype.uint32, 32]  # type: ignore
    __f_2319175490318793746: [datatype.uint32, 32]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int, int, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        self.__f_2319175490318793746 = int(0)
        cf_str += '>u32'
        self.__f_7839095738514289283 = int(0)
        cf_str += '>u32'
        self.__f_972799269597490421 = int(0)
        cf_str += '>u32'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(2)

    def fields(
        self,
        f_972799269597490421: int = None,
        f_7839095738514289283: int = None,
        f_2319175490318793746: int = None,
    ):
        if f_972799269597490421:
            self.f_972799269597490421 = f_972799269597490421
        if f_7839095738514289283:
            self.f_7839095738514289283 = f_7839095738514289283
        if f_2319175490318793746:
            self.f_2319175490318793746 = f_2319175490318793746
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_2319175490318793746),
            int(self.f_7839095738514289283),
            int(self.f_972799269597490421),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 13
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x2
        (
            self.f_2319175490318793746,
            self.f_7839095738514289283,
            self.f_972799269597490421,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_4723717955423805745(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_4723717955423805745().fields(\n'
        res += '\tf_972799269597490421 = %s ,\n' % str(
            self.f_972799269597490421)
        res += '\tf_7839095738514289283 = %s ,\n' % str(
            self.f_7839095738514289283)
        res += '\tf_2319175490318793746 = %s ,\n' % str(
            self.f_2319175490318793746)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 13

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_972799269597490421(self):
        return self.__f_972799269597490421

    def __set_f_972799269597490421(self, value):
        assert int(value) < 2**32

        assert int(value) >= 0

        self.__f_972799269597490421 = int(value)

    def __get_f_7839095738514289283(self):
        return self.__f_7839095738514289283

    def __set_f_7839095738514289283(self, value):
        assert int(value) < 2**32

        assert int(value) >= 0

        self.__f_7839095738514289283 = int(value)

    def __get_f_2319175490318793746(self):
        return self.__f_2319175490318793746

    def __set_f_2319175490318793746(self, value):
        assert int(value) < 2**32

        assert int(value) >= 0

        self.__f_2319175490318793746 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_972799269597490421 = property(__get_f_972799269597490421,
                                    __set_f_972799269597490421)
    f_7839095738514289283 = property(__get_f_7839095738514289283,
                                     __set_f_7839095738514289283)
    f_2319175490318793746 = property(__get_f_2319175490318793746,
                                     __set_f_2319175490318793746)


class inst_i_328345304491746530(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_972799269597490421: [datatype.uint32, 32]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        self.__f_972799269597490421 = int(0)
        cf_str += '>u32'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(3)

    def fields(
        self,
        f_972799269597490421: int = None,
    ):
        if f_972799269597490421:
            self.f_972799269597490421 = f_972799269597490421
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_972799269597490421),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 5
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x3
        (
            self.f_972799269597490421,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_328345304491746530(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_328345304491746530().fields(\n'
        res += '\tf_972799269597490421 = %s ,\n' % str(
            self.f_972799269597490421)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 5

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_972799269597490421(self):
        return self.__f_972799269597490421

    def __set_f_972799269597490421(self, value):
        assert int(value) < 2**32

        assert int(value) >= 0

        self.__f_972799269597490421 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_972799269597490421 = property(__get_f_972799269597490421,
                                    __set_f_972799269597490421)


class inst_i_8790047992392043228(serialize_struct):

    __f_3576753080704587277: [OPCODE, 8]  # type: ignore

    def __init__(self, value: Union[bytes, str] = None, hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        self.__f_3576753080704587277 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        self.opcode = OPCODE(4)

    def fields(self,):
        return self

    def pack(self) -> bytes:
        return self.cf.pack(int(self.f_3576753080704587277),)[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 1
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x4
        (self.f_3576753080704587277,) = res

    def __repr__(self):
        return 'inst_i_8790047992392043228(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_8790047992392043228().fields(\n'
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 1

    # getter and setters

    def __get_f_3576753080704587277(self):
        return self.__f_3576753080704587277

    def __set_f_3576753080704587277(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_3576753080704587277 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    f_3576753080704587277 = property(__get_f_3576753080704587277,
                                     __set_f_3576753080704587277)


class inst_i_7155768076259033706(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_2112052519892767027: [int, 4]  # type: ignore
    __f_3943017454048580119: [int, 3]  # type: ignore
    __f_3905006341331977103: [MMU_CONF_WIDTH, 2]  # type: ignore
    __f_6408653933611170285: [int, 14]  # type: ignore
    __f_8286030622146308258: [int, 14]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int, int, MMU_CONF_WIDTH, int, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(3)

        self.__f_8286030622146308258 = int(0)
        cf_str += '>u14'
        self.__f_6408653933611170285 = int(0)
        cf_str += '>u14'
        self.__f_3905006341331977103 = MMU_CONF_WIDTH(0)
        cf_str += '>u2'
        self.__f_3943017454048580119 = int(0)
        cf_str += '>u3'
        self.__f_2112052519892767027 = int(0)
        cf_str += '>u4'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(5)

    def fields(
        self,
        f_2112052519892767027: int = None,
        f_3943017454048580119: int = None,
        f_3905006341331977103: MMU_CONF_WIDTH = None,
        f_6408653933611170285: int = None,
        f_8286030622146308258: int = None,
    ):
        if f_2112052519892767027:
            self.f_2112052519892767027 = f_2112052519892767027
        if f_3943017454048580119:
            self.f_3943017454048580119 = f_3943017454048580119
        if f_3905006341331977103:
            self.f_3905006341331977103 = f_3905006341331977103
        if f_6408653933611170285:
            self.f_6408653933611170285 = f_6408653933611170285
        if f_8286030622146308258:
            self.f_8286030622146308258 = f_8286030622146308258
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_8286030622146308258),
            int(self.f_6408653933611170285),
            int(self.f_3905006341331977103),
            int(self.f_3943017454048580119),
            int(self.f_2112052519892767027),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 6
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x5
        (
            self.f_8286030622146308258,
            self.f_6408653933611170285,
            self.f_3905006341331977103,
            self.f_3943017454048580119,
            self.f_2112052519892767027,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_7155768076259033706(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_7155768076259033706().fields(\n'
        res += '\tf_2112052519892767027 = %s ,\n' % str(
            self.f_2112052519892767027)
        res += '\tf_3943017454048580119 = %s ,\n' % str(
            self.f_3943017454048580119)
        res += '\tf_3905006341331977103 = %s ,\n' % str(
            self.f_3905006341331977103)
        res += '\tf_6408653933611170285 = %s ,\n' % str(
            self.f_6408653933611170285)
        res += '\tf_8286030622146308258 = %s ,\n' % str(
            self.f_8286030622146308258)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 6

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_2112052519892767027(self):
        return self.__f_2112052519892767027

    def __set_f_2112052519892767027(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_2112052519892767027 = int(value)

    def __get_f_3943017454048580119(self):
        return self.__f_3943017454048580119

    def __set_f_3943017454048580119(self, value):
        assert int(value) < 2**3

        assert int(value) >= 0

        self.__f_3943017454048580119 = int(value)

    def __get_f_3905006341331977103(self):
        return self.__f_3905006341331977103

    def __set_f_3905006341331977103(self, value):

        assert (isinstance(value, (int, MMU_CONF_WIDTH)))
        self.__f_3905006341331977103 = value if isinstance(
            value, MMU_CONF_WIDTH) else MMU_CONF_WIDTH(value)

    def __get_f_6408653933611170285(self):
        return self.__f_6408653933611170285

    def __set_f_6408653933611170285(self, value):
        assert int(value) < 12287
        assert int(value) >= 0

        self.__f_6408653933611170285 = int(value)

    def __get_f_8286030622146308258(self):
        return self.__f_8286030622146308258

    def __set_f_8286030622146308258(self, value):
        assert int(value) < 2**14

        assert int(value) > 1
        self.__f_8286030622146308258 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_2112052519892767027 = property(__get_f_2112052519892767027,
                                     __set_f_2112052519892767027)
    f_3943017454048580119 = property(__get_f_3943017454048580119,
                                     __set_f_3943017454048580119)
    f_3905006341331977103 = property(__get_f_3905006341331977103,
                                     __set_f_3905006341331977103)
    f_6408653933611170285 = property(__get_f_6408653933611170285,
                                     __set_f_6408653933611170285)
    f_8286030622146308258 = property(__get_f_8286030622146308258,
                                     __set_f_8286030622146308258)


class inst_i_4539906387927636499(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_5085793024541575481: [int, 6]  # type: ignore
    __f_3217332499044511084: [int, 1]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(1)

        self.__f_3217332499044511084 = int(0)
        cf_str += '>u1'
        self.__f_5085793024541575481 = int(0)
        cf_str += '>u6'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(8)

    def fields(
        self,
        f_5085793024541575481: int = None,
        f_3217332499044511084: int = None,
    ):
        if f_5085793024541575481:
            self.f_5085793024541575481 = f_5085793024541575481
        if f_3217332499044511084:
            self.f_3217332499044511084 = f_3217332499044511084
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_3217332499044511084),
            int(self.f_5085793024541575481),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 2
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x8
        (
            self.f_3217332499044511084,
            self.f_5085793024541575481,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_4539906387927636499(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_4539906387927636499().fields(\n'
        res += '\tf_5085793024541575481 = %s ,\n' % str(
            self.f_5085793024541575481)
        res += '\tf_3217332499044511084 = %s ,\n' % str(
            self.f_3217332499044511084)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 2

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_5085793024541575481(self):
        return self.__f_5085793024541575481

    def __set_f_5085793024541575481(self, value):
        assert int(value) < 2**6

        assert int(value) >= 0

        self.__f_5085793024541575481 = int(value)

    def __get_f_3217332499044511084(self):
        return self.__f_3217332499044511084

    def __set_f_3217332499044511084(self, value):
        assert int(value) < 2**1

        assert int(value) >= 0

        self.__f_3217332499044511084 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_5085793024541575481 = property(__get_f_5085793024541575481,
                                     __set_f_5085793024541575481)
    f_3217332499044511084 = property(__get_f_3217332499044511084,
                                     __set_f_3217332499044511084)


class inst_i_4968684677827927616(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_8522342661322622465: [datatype.uint16, 16]  # type: ignore
    __f_3676797385440794520: [datatype.uint16, 16]  # type: ignore
    __f_1654969283327896294: [datatype.uint16, 16]  # type: ignore
    __f_860775722809473967: [datatype.uint16, 16]  # type: ignore
    __f_1218174442252260153: [STRIDE_GLB, 64]  # type: ignore
    __f_2112052519892767027: [int, 4]  # type: ignore
    __f_6766582184502734391: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_5550496230836118772: [QUAN_SIGNED, 1]  # type: ignore
    __f_3913792219024292053: [PRECISION, 2]  # type: ignore
    __f_6532188106183563848: [PRECISION_DDR, 3]  # type: ignore
    __f_8617447463546780470: [QUAN_TYPE, 1]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int, int, int, int, STRIDE_GLB, int,
                               ADDR_GLB_8_WITH_BANK, QUAN_SIGNED, PRECISION,
                               PRECISION_DDR, QUAN_TYPE,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(4)

        self.__f_8617447463546780470 = QUAN_TYPE(0)
        cf_str += '>u1'
        self.__f_6532188106183563848 = PRECISION_DDR(0)
        cf_str += '>u3'
        self.__f_3913792219024292053 = PRECISION(0)
        cf_str += '>u2'
        self.__f_5550496230836118772 = QUAN_SIGNED(0)
        cf_str += '>u1'
        self.__f_6766582184502734391 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_2112052519892767027 = int(0)
        cf_str += '>u4'
        self.__f_1218174442252260153 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_860775722809473967 = int(0)
        cf_str += '>u16'
        self.__f_1654969283327896294 = int(0)
        cf_str += '>u16'
        self.__f_3676797385440794520 = int(0)
        cf_str += '>u16'
        self.__f_8522342661322622465 = int(0)
        cf_str += '>u16'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(16)

    def fields(
        self,
        f_8522342661322622465: int = None,
        f_3676797385440794520: int = None,
        f_1654969283327896294: int = None,
        f_860775722809473967: int = None,
        f_1218174442252260153: STRIDE_GLB = None,
        f_2112052519892767027: int = None,
        f_6766582184502734391: ADDR_GLB_8_WITH_BANK = None,
        f_5550496230836118772: QUAN_SIGNED = None,
        f_3913792219024292053: PRECISION = None,
        f_6532188106183563848: PRECISION_DDR = None,
        f_8617447463546780470: QUAN_TYPE = None,
    ):
        if f_8522342661322622465:
            self.f_8522342661322622465 = f_8522342661322622465
        if f_3676797385440794520:
            self.f_3676797385440794520 = f_3676797385440794520
        if f_1654969283327896294:
            self.f_1654969283327896294 = f_1654969283327896294
        if f_860775722809473967:
            self.f_860775722809473967 = f_860775722809473967
        if f_1218174442252260153:
            self.f_1218174442252260153 = f_1218174442252260153
        if f_2112052519892767027:
            self.f_2112052519892767027 = f_2112052519892767027
        if f_6766582184502734391:
            self.f_6766582184502734391 = f_6766582184502734391
        if f_5550496230836118772:
            self.f_5550496230836118772 = f_5550496230836118772
        if f_3913792219024292053:
            self.f_3913792219024292053 = f_3913792219024292053
        if f_6532188106183563848:
            self.f_6532188106183563848 = f_6532188106183563848
        if f_8617447463546780470:
            self.f_8617447463546780470 = f_8617447463546780470
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_8617447463546780470),
            int(self.f_6532188106183563848),
            int(self.f_3913792219024292053),
            int(self.f_5550496230836118772),
            int(self.f_6766582184502734391),
            int(self.f_2112052519892767027),
            int(self.f_1218174442252260153),
            int(self.f_860775722809473967),
            int(self.f_1654969283327896294),
            int(self.f_3676797385440794520),
            int(self.f_8522342661322622465),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 22
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x10
        (
            self.f_8617447463546780470,
            self.f_6532188106183563848,
            self.f_3913792219024292053,
            self.f_5550496230836118772,
            self.f_6766582184502734391,
            self.f_2112052519892767027,
            self.f_1218174442252260153,
            self.f_860775722809473967,
            self.f_1654969283327896294,
            self.f_3676797385440794520,
            self.f_8522342661322622465,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_4968684677827927616(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_4968684677827927616().fields(\n'
        res += '\tf_8522342661322622465 = %s ,\n' % str(
            self.f_8522342661322622465)
        res += '\tf_3676797385440794520 = %s ,\n' % str(
            self.f_3676797385440794520)
        res += '\tf_1654969283327896294 = %s ,\n' % str(
            self.f_1654969283327896294)
        res += '\tf_860775722809473967 = %s ,\n' % str(
            self.f_860775722809473967)
        res += '\tf_1218174442252260153 = %s ,\n' % str(
            self.f_1218174442252260153)
        res += '\tf_2112052519892767027 = %s ,\n' % str(
            self.f_2112052519892767027)
        res += '\tf_6766582184502734391 = %s ,\n' % str(
            self.f_6766582184502734391)
        res += '\tf_5550496230836118772 = %s ,\n' % str(
            self.f_5550496230836118772)
        res += '\tf_3913792219024292053 = %s ,\n' % str(
            self.f_3913792219024292053)
        res += '\tf_6532188106183563848 = %s ,\n' % str(
            self.f_6532188106183563848)
        res += '\tf_8617447463546780470 = %s ,\n' % str(
            self.f_8617447463546780470)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 22

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_8522342661322622465(self):
        return self.__f_8522342661322622465

    def __set_f_8522342661322622465(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8522342661322622465 = int(value)

    def __get_f_3676797385440794520(self):
        return self.__f_3676797385440794520

    def __set_f_3676797385440794520(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_3676797385440794520 = int(value)

    def __get_f_1654969283327896294(self):
        return self.__f_1654969283327896294

    def __set_f_1654969283327896294(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1654969283327896294 = int(value)

    def __get_f_860775722809473967(self):
        return self.__f_860775722809473967

    def __set_f_860775722809473967(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_860775722809473967 = int(value)

    def __get_f_1218174442252260153(self):
        return self.__f_1218174442252260153

    def __set_f_1218174442252260153(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_1218174442252260153 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_2112052519892767027(self):
        return self.__f_2112052519892767027

    def __set_f_2112052519892767027(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_2112052519892767027 = int(value)

    def __get_f_6766582184502734391(self):
        return self.__f_6766582184502734391

    def __set_f_6766582184502734391(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_6766582184502734391 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_5550496230836118772(self):
        return self.__f_5550496230836118772

    def __set_f_5550496230836118772(self, value):

        assert (isinstance(value, (int, QUAN_SIGNED)))
        self.__f_5550496230836118772 = value if isinstance(
            value, QUAN_SIGNED) else QUAN_SIGNED(value)

    def __get_f_3913792219024292053(self):
        return self.__f_3913792219024292053

    def __set_f_3913792219024292053(self, value):

        assert (isinstance(value, (int, PRECISION)))
        self.__f_3913792219024292053 = value if isinstance(
            value, PRECISION) else PRECISION(value)

    def __get_f_6532188106183563848(self):
        return self.__f_6532188106183563848

    def __set_f_6532188106183563848(self, value):

        assert (isinstance(value, (int, PRECISION_DDR)))
        self.__f_6532188106183563848 = value if isinstance(
            value, PRECISION_DDR) else PRECISION_DDR(value)

    def __get_f_8617447463546780470(self):
        return self.__f_8617447463546780470

    def __set_f_8617447463546780470(self, value):

        assert (isinstance(value, (int, QUAN_TYPE)))
        self.__f_8617447463546780470 = value if isinstance(
            value, QUAN_TYPE) else QUAN_TYPE(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_8522342661322622465 = property(__get_f_8522342661322622465,
                                     __set_f_8522342661322622465)
    f_3676797385440794520 = property(__get_f_3676797385440794520,
                                     __set_f_3676797385440794520)
    f_1654969283327896294 = property(__get_f_1654969283327896294,
                                     __set_f_1654969283327896294)
    f_860775722809473967 = property(__get_f_860775722809473967,
                                    __set_f_860775722809473967)
    f_1218174442252260153 = property(__get_f_1218174442252260153,
                                     __set_f_1218174442252260153)
    f_2112052519892767027 = property(__get_f_2112052519892767027,
                                     __set_f_2112052519892767027)
    f_6766582184502734391 = property(__get_f_6766582184502734391,
                                     __set_f_6766582184502734391)
    f_5550496230836118772 = property(__get_f_5550496230836118772,
                                     __set_f_5550496230836118772)
    f_3913792219024292053 = property(__get_f_3913792219024292053,
                                     __set_f_3913792219024292053)
    f_6532188106183563848 = property(__get_f_6532188106183563848,
                                     __set_f_6532188106183563848)
    f_8617447463546780470 = property(__get_f_8617447463546780470,
                                     __set_f_8617447463546780470)


class inst_i_6647669131517538538(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_6920772091196212887: [CCRCLR, 8]  # type: ignore
    __f_1885779890895099474: [CCRCLR, 8]  # type: ignore
    __f_1851582658599760477: [CCRSET, 11]  # type: ignore
    __f_4535149732094779661: [ADDR, 32]  # type: ignore
    __f_581203445514181141: [ADDR_GLB_8_WITHOUT_BANK, 21]  # type: ignore
    __f_1449988654089269400: [datatype.uint16, 16]  # type: ignore
    __f_8538332288708448876: [datatype.uint16, 16]  # type: ignore
    __f_8660001712953173509: [datatype.uint16, 16]  # type: ignore
    __f_2401380060870497267: [datatype.uint16, 16]  # type: ignore
    __f_816100931824639168: [int, 2]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, CCRCLR, CCRSET, ADDR,
                               ADDR_GLB_8_WITHOUT_BANK, int, int, int, int,
                               int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(6)

        self.__f_816100931824639168 = int(0)
        cf_str += '>u2'
        self.__f_2401380060870497267 = int(0)
        cf_str += '>u16'
        self.__f_8660001712953173509 = int(0)
        cf_str += '>u16'
        self.__f_8538332288708448876 = int(0)
        cf_str += '>u16'
        self.__f_1449988654089269400 = int(0)
        cf_str += '>u16'
        self.__f_581203445514181141 = ADDR_GLB_8_WITHOUT_BANK(0)
        cf_str += '>u21'
        self.__f_4535149732094779661 = ADDR(0)
        cf_str += '>u32'
        self.__f_1851582658599760477 = CCRSET(0)
        cf_str += '>u11'
        self.__f_1885779890895099474 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_6920772091196212887 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(17)

    def fields(
        self,
        f_6920772091196212887: CCRCLR = None,
        f_1885779890895099474: CCRCLR = None,
        f_1851582658599760477: CCRSET = None,
        f_4535149732094779661: ADDR = None,
        f_581203445514181141: ADDR_GLB_8_WITHOUT_BANK = None,
        f_1449988654089269400: int = None,
        f_8538332288708448876: int = None,
        f_8660001712953173509: int = None,
        f_2401380060870497267: int = None,
        f_816100931824639168: int = None,
    ):
        if f_6920772091196212887:
            self.f_6920772091196212887 = f_6920772091196212887
        if f_1885779890895099474:
            self.f_1885779890895099474 = f_1885779890895099474
        if f_1851582658599760477:
            self.f_1851582658599760477 = f_1851582658599760477
        if f_4535149732094779661:
            self.f_4535149732094779661 = f_4535149732094779661
        if f_581203445514181141:
            self.f_581203445514181141 = f_581203445514181141
        if f_1449988654089269400:
            self.f_1449988654089269400 = f_1449988654089269400
        if f_8538332288708448876:
            self.f_8538332288708448876 = f_8538332288708448876
        if f_8660001712953173509:
            self.f_8660001712953173509 = f_8660001712953173509
        if f_2401380060870497267:
            self.f_2401380060870497267 = f_2401380060870497267
        if f_816100931824639168:
            self.f_816100931824639168 = f_816100931824639168
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_816100931824639168),
            int(self.f_2401380060870497267),
            int(self.f_8660001712953173509),
            int(self.f_8538332288708448876),
            int(self.f_1449988654089269400),
            int(self.f_581203445514181141),
            int(self.f_4535149732094779661),
            int(self.f_1851582658599760477),
            int(self.f_1885779890895099474),
            int(self.f_6920772091196212887),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 20
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x11
        (
            self.f_816100931824639168,
            self.f_2401380060870497267,
            self.f_8660001712953173509,
            self.f_8538332288708448876,
            self.f_1449988654089269400,
            self.f_581203445514181141,
            self.f_4535149732094779661,
            self.f_1851582658599760477,
            self.f_1885779890895099474,
            self.f_6920772091196212887,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_6647669131517538538(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_6647669131517538538().fields(\n'
        res += '\tf_6920772091196212887 = %s ,\n' % str(
            self.f_6920772091196212887)
        res += '\tf_1885779890895099474 = %s ,\n' % str(
            self.f_1885779890895099474)
        res += '\tf_1851582658599760477 = %s ,\n' % str(
            self.f_1851582658599760477)
        res += '\tf_4535149732094779661 = %s ,\n' % str(
            self.f_4535149732094779661)
        res += '\tf_581203445514181141 = %s ,\n' % str(
            self.f_581203445514181141)
        res += '\tf_1449988654089269400 = %s ,\n' % str(
            self.f_1449988654089269400)
        res += '\tf_8538332288708448876 = %s ,\n' % str(
            self.f_8538332288708448876)
        res += '\tf_8660001712953173509 = %s ,\n' % str(
            self.f_8660001712953173509)
        res += '\tf_2401380060870497267 = %s ,\n' % str(
            self.f_2401380060870497267)
        res += '\tf_816100931824639168 = %s ,\n' % str(
            self.f_816100931824639168)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 20

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_6920772091196212887(self):
        return self.__f_6920772091196212887

    def __set_f_6920772091196212887(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_6920772091196212887 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1885779890895099474(self):
        return self.__f_1885779890895099474

    def __set_f_1885779890895099474(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_1885779890895099474 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1851582658599760477(self):
        return self.__f_1851582658599760477

    def __set_f_1851582658599760477(self, value):

        assert (isinstance(value, (int, CCRSET)))
        self.__f_1851582658599760477 = value if isinstance(
            value, CCRSET) else CCRSET(value)

    def __get_f_4535149732094779661(self):
        return self.__f_4535149732094779661

    def __set_f_4535149732094779661(self, value):

        assert (isinstance(value, (int, ADDR)))
        self.__f_4535149732094779661 = value if isinstance(
            value, ADDR) else ADDR(value)

    def __get_f_581203445514181141(self):
        return self.__f_581203445514181141

    def __set_f_581203445514181141(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITHOUT_BANK)))
        self.__f_581203445514181141 = value if isinstance(
            value, ADDR_GLB_8_WITHOUT_BANK) else ADDR_GLB_8_WITHOUT_BANK(value)

    def __get_f_1449988654089269400(self):
        return self.__f_1449988654089269400

    def __set_f_1449988654089269400(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1449988654089269400 = int(value)

    def __get_f_8538332288708448876(self):
        return self.__f_8538332288708448876

    def __set_f_8538332288708448876(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8538332288708448876 = int(value)

    def __get_f_8660001712953173509(self):
        return self.__f_8660001712953173509

    def __set_f_8660001712953173509(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8660001712953173509 = int(value)

    def __get_f_2401380060870497267(self):
        return self.__f_2401380060870497267

    def __set_f_2401380060870497267(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_2401380060870497267 = int(value)

    def __get_f_816100931824639168(self):
        return self.__f_816100931824639168

    def __set_f_816100931824639168(self, value):
        assert int(value) < 2**2

        assert int(value) >= 0

        self.__f_816100931824639168 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_6920772091196212887 = property(__get_f_6920772091196212887,
                                     __set_f_6920772091196212887)
    f_1885779890895099474 = property(__get_f_1885779890895099474,
                                     __set_f_1885779890895099474)
    f_1851582658599760477 = property(__get_f_1851582658599760477,
                                     __set_f_1851582658599760477)
    f_4535149732094779661 = property(__get_f_4535149732094779661,
                                     __set_f_4535149732094779661)
    f_581203445514181141 = property(__get_f_581203445514181141,
                                    __set_f_581203445514181141)
    f_1449988654089269400 = property(__get_f_1449988654089269400,
                                     __set_f_1449988654089269400)
    f_8538332288708448876 = property(__get_f_8538332288708448876,
                                     __set_f_8538332288708448876)
    f_8660001712953173509 = property(__get_f_8660001712953173509,
                                     __set_f_8660001712953173509)
    f_2401380060870497267 = property(__get_f_2401380060870497267,
                                     __set_f_2401380060870497267)
    f_816100931824639168 = property(__get_f_816100931824639168,
                                    __set_f_816100931824639168)


class inst_i_6703668108300758238(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_6920772091196212887: [CCRCLR, 8]  # type: ignore
    __f_1885779890895099474: [CCRCLR, 8]  # type: ignore
    __f_1851582658599760477: [CCRSET, 11]  # type: ignore
    __f_4535149732094779661: [ADDR, 32]  # type: ignore
    __f_581203445514181141: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_8504158210894135380: [int, 21]  # type: ignore
    __f_6766582184502734391: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_967006719681078271: [datatype.uint16, 16]  # type: ignore
    __f_8538332288708448876: [datatype.uint16, 16]  # type: ignore
    __f_816100931824639168: [int, 2]  # type: ignore
    __f_5550496230836118772: [QUAN_SIGNED, 1]  # type: ignore
    __f_3913792219024292053: [PRECISION, 2]  # type: ignore
    __f_6532188106183563848: [PRECISION_DDR, 3]  # type: ignore
    __f_3378213490212613949: [int, 1]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, CCRCLR, CCRSET, ADDR,
                               ADDR_GLB_8_WITH_BANK, int, ADDR_GLB_8_WITH_BANK,
                               int, int, int, QUAN_SIGNED, PRECISION,
                               PRECISION_DDR, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(5)

        self.__f_3378213490212613949 = int(0)
        cf_str += '>u1'
        self.__f_6532188106183563848 = PRECISION_DDR(0)
        cf_str += '>u3'
        self.__f_3913792219024292053 = PRECISION(0)
        cf_str += '>u2'
        self.__f_5550496230836118772 = QUAN_SIGNED(0)
        cf_str += '>u1'
        self.__f_816100931824639168 = int(0)
        cf_str += '>u2'
        self.__f_8538332288708448876 = int(0)
        cf_str += '>u16'
        self.__f_967006719681078271 = int(0)
        cf_str += '>u16'
        self.__f_6766582184502734391 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_8504158210894135380 = int(0)
        cf_str += '>u21'
        self.__f_581203445514181141 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_4535149732094779661 = ADDR(0)
        cf_str += '>u32'
        self.__f_1851582658599760477 = CCRSET(0)
        cf_str += '>u11'
        self.__f_1885779890895099474 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_6920772091196212887 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(18)

    def fields(
        self,
        f_6920772091196212887: CCRCLR = None,
        f_1885779890895099474: CCRCLR = None,
        f_1851582658599760477: CCRSET = None,
        f_4535149732094779661: ADDR = None,
        f_581203445514181141: ADDR_GLB_8_WITH_BANK = None,
        f_8504158210894135380: int = None,
        f_6766582184502734391: ADDR_GLB_8_WITH_BANK = None,
        f_967006719681078271: int = None,
        f_8538332288708448876: int = None,
        f_816100931824639168: int = None,
        f_5550496230836118772: QUAN_SIGNED = None,
        f_3913792219024292053: PRECISION = None,
        f_6532188106183563848: PRECISION_DDR = None,
        f_3378213490212613949: int = None,
    ):
        if f_6920772091196212887:
            self.f_6920772091196212887 = f_6920772091196212887
        if f_1885779890895099474:
            self.f_1885779890895099474 = f_1885779890895099474
        if f_1851582658599760477:
            self.f_1851582658599760477 = f_1851582658599760477
        if f_4535149732094779661:
            self.f_4535149732094779661 = f_4535149732094779661
        if f_581203445514181141:
            self.f_581203445514181141 = f_581203445514181141
        if f_8504158210894135380:
            self.f_8504158210894135380 = f_8504158210894135380
        if f_6766582184502734391:
            self.f_6766582184502734391 = f_6766582184502734391
        if f_967006719681078271:
            self.f_967006719681078271 = f_967006719681078271
        if f_8538332288708448876:
            self.f_8538332288708448876 = f_8538332288708448876
        if f_816100931824639168:
            self.f_816100931824639168 = f_816100931824639168
        if f_5550496230836118772:
            self.f_5550496230836118772 = f_5550496230836118772
        if f_3913792219024292053:
            self.f_3913792219024292053 = f_3913792219024292053
        if f_6532188106183563848:
            self.f_6532188106183563848 = f_6532188106183563848
        if f_3378213490212613949:
            self.f_3378213490212613949 = f_3378213490212613949
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_3378213490212613949),
            int(self.f_6532188106183563848),
            int(self.f_3913792219024292053),
            int(self.f_5550496230836118772),
            int(self.f_816100931824639168),
            int(self.f_8538332288708448876),
            int(self.f_967006719681078271),
            int(self.f_6766582184502734391),
            int(self.f_8504158210894135380),
            int(self.f_581203445514181141),
            int(self.f_4535149732094779661),
            int(self.f_1851582658599760477),
            int(self.f_1885779890895099474),
            int(self.f_6920772091196212887),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 23
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x12
        (
            self.f_3378213490212613949,
            self.f_6532188106183563848,
            self.f_3913792219024292053,
            self.f_5550496230836118772,
            self.f_816100931824639168,
            self.f_8538332288708448876,
            self.f_967006719681078271,
            self.f_6766582184502734391,
            self.f_8504158210894135380,
            self.f_581203445514181141,
            self.f_4535149732094779661,
            self.f_1851582658599760477,
            self.f_1885779890895099474,
            self.f_6920772091196212887,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_6703668108300758238(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_6703668108300758238().fields(\n'
        res += '\tf_6920772091196212887 = %s ,\n' % str(
            self.f_6920772091196212887)
        res += '\tf_1885779890895099474 = %s ,\n' % str(
            self.f_1885779890895099474)
        res += '\tf_1851582658599760477 = %s ,\n' % str(
            self.f_1851582658599760477)
        res += '\tf_4535149732094779661 = %s ,\n' % str(
            self.f_4535149732094779661)
        res += '\tf_581203445514181141 = %s ,\n' % str(
            self.f_581203445514181141)
        res += '\tf_8504158210894135380 = %s ,\n' % str(
            self.f_8504158210894135380)
        res += '\tf_6766582184502734391 = %s ,\n' % str(
            self.f_6766582184502734391)
        res += '\tf_967006719681078271 = %s ,\n' % str(
            self.f_967006719681078271)
        res += '\tf_8538332288708448876 = %s ,\n' % str(
            self.f_8538332288708448876)
        res += '\tf_816100931824639168 = %s ,\n' % str(
            self.f_816100931824639168)
        res += '\tf_5550496230836118772 = %s ,\n' % str(
            self.f_5550496230836118772)
        res += '\tf_3913792219024292053 = %s ,\n' % str(
            self.f_3913792219024292053)
        res += '\tf_6532188106183563848 = %s ,\n' % str(
            self.f_6532188106183563848)
        res += '\tf_3378213490212613949 = %s ,\n' % str(
            self.f_3378213490212613949)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 23

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_6920772091196212887(self):
        return self.__f_6920772091196212887

    def __set_f_6920772091196212887(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_6920772091196212887 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1885779890895099474(self):
        return self.__f_1885779890895099474

    def __set_f_1885779890895099474(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_1885779890895099474 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1851582658599760477(self):
        return self.__f_1851582658599760477

    def __set_f_1851582658599760477(self, value):

        assert (isinstance(value, (int, CCRSET)))
        self.__f_1851582658599760477 = value if isinstance(
            value, CCRSET) else CCRSET(value)

    def __get_f_4535149732094779661(self):
        return self.__f_4535149732094779661

    def __set_f_4535149732094779661(self, value):

        assert (isinstance(value, (int, ADDR)))
        self.__f_4535149732094779661 = value if isinstance(
            value, ADDR) else ADDR(value)

    def __get_f_581203445514181141(self):
        return self.__f_581203445514181141

    def __set_f_581203445514181141(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_581203445514181141 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_8504158210894135380(self):
        return self.__f_8504158210894135380

    def __set_f_8504158210894135380(self, value):
        assert int(value) < 2**21

        assert int(value) >= 0

        self.__f_8504158210894135380 = int(value)

    def __get_f_6766582184502734391(self):
        return self.__f_6766582184502734391

    def __set_f_6766582184502734391(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_6766582184502734391 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_967006719681078271(self):
        return self.__f_967006719681078271

    def __set_f_967006719681078271(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_967006719681078271 = int(value)

    def __get_f_8538332288708448876(self):
        return self.__f_8538332288708448876

    def __set_f_8538332288708448876(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8538332288708448876 = int(value)

    def __get_f_816100931824639168(self):
        return self.__f_816100931824639168

    def __set_f_816100931824639168(self, value):
        assert int(value) < 2**2

        assert int(value) >= 0

        self.__f_816100931824639168 = int(value)

    def __get_f_5550496230836118772(self):
        return self.__f_5550496230836118772

    def __set_f_5550496230836118772(self, value):

        assert (isinstance(value, (int, QUAN_SIGNED)))
        self.__f_5550496230836118772 = value if isinstance(
            value, QUAN_SIGNED) else QUAN_SIGNED(value)

    def __get_f_3913792219024292053(self):
        return self.__f_3913792219024292053

    def __set_f_3913792219024292053(self, value):

        assert (isinstance(value, (int, PRECISION)))
        self.__f_3913792219024292053 = value if isinstance(
            value, PRECISION) else PRECISION(value)

    def __get_f_6532188106183563848(self):
        return self.__f_6532188106183563848

    def __set_f_6532188106183563848(self, value):

        assert (isinstance(value, (int, PRECISION_DDR)))
        self.__f_6532188106183563848 = value if isinstance(
            value, PRECISION_DDR) else PRECISION_DDR(value)

    def __get_f_3378213490212613949(self):
        return self.__f_3378213490212613949

    def __set_f_3378213490212613949(self, value):
        assert int(value) < 2**1

        assert int(value) >= 0

        self.__f_3378213490212613949 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_6920772091196212887 = property(__get_f_6920772091196212887,
                                     __set_f_6920772091196212887)
    f_1885779890895099474 = property(__get_f_1885779890895099474,
                                     __set_f_1885779890895099474)
    f_1851582658599760477 = property(__get_f_1851582658599760477,
                                     __set_f_1851582658599760477)
    f_4535149732094779661 = property(__get_f_4535149732094779661,
                                     __set_f_4535149732094779661)
    f_581203445514181141 = property(__get_f_581203445514181141,
                                    __set_f_581203445514181141)
    f_8504158210894135380 = property(__get_f_8504158210894135380,
                                     __set_f_8504158210894135380)
    f_6766582184502734391 = property(__get_f_6766582184502734391,
                                     __set_f_6766582184502734391)
    f_967006719681078271 = property(__get_f_967006719681078271,
                                    __set_f_967006719681078271)
    f_8538332288708448876 = property(__get_f_8538332288708448876,
                                     __set_f_8538332288708448876)
    f_816100931824639168 = property(__get_f_816100931824639168,
                                    __set_f_816100931824639168)
    f_5550496230836118772 = property(__get_f_5550496230836118772,
                                     __set_f_5550496230836118772)
    f_3913792219024292053 = property(__get_f_3913792219024292053,
                                     __set_f_3913792219024292053)
    f_6532188106183563848 = property(__get_f_6532188106183563848,
                                     __set_f_6532188106183563848)
    f_3378213490212613949 = property(__get_f_3378213490212613949,
                                     __set_f_3378213490212613949)


class inst_i_9152920230794971550(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_3068946584496572486: [ADDR, 32]  # type: ignore
    __f_1276250833917656531: [ADDR, 32]  # type: ignore
    __f_510303099668681797: [ADDR, 32]  # type: ignore
    __f_6214993069921897693: [int, 4]  # type: ignore
    __f_3392370045775382312: [SPARSIFIED, 1]  # type: ignore
    __f_1734190238197517228: [COMPRESSED, 1]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[ADDR, ADDR, ADDR, int, SPARSIFIED,
                               COMPRESSED,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(2)

        self.__f_1734190238197517228 = COMPRESSED(0)
        cf_str += '>u1'
        self.__f_3392370045775382312 = SPARSIFIED(0)
        cf_str += '>u1'
        self.__f_6214993069921897693 = int(0)
        cf_str += '>u4'
        self.__f_510303099668681797 = ADDR(0)
        cf_str += '>u32'
        self.__f_1276250833917656531 = ADDR(0)
        cf_str += '>u32'
        self.__f_3068946584496572486 = ADDR(0)
        cf_str += '>u32'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(20)

    def fields(
        self,
        f_3068946584496572486: ADDR = None,
        f_1276250833917656531: ADDR = None,
        f_510303099668681797: ADDR = None,
        f_6214993069921897693: int = None,
        f_3392370045775382312: SPARSIFIED = None,
        f_1734190238197517228: COMPRESSED = None,
    ):
        if f_3068946584496572486:
            self.f_3068946584496572486 = f_3068946584496572486
        if f_1276250833917656531:
            self.f_1276250833917656531 = f_1276250833917656531
        if f_510303099668681797:
            self.f_510303099668681797 = f_510303099668681797
        if f_6214993069921897693:
            self.f_6214993069921897693 = f_6214993069921897693
        if f_3392370045775382312:
            self.f_3392370045775382312 = f_3392370045775382312
        if f_1734190238197517228:
            self.f_1734190238197517228 = f_1734190238197517228
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_1734190238197517228),
            int(self.f_3392370045775382312),
            int(self.f_6214993069921897693),
            int(self.f_510303099668681797),
            int(self.f_1276250833917656531),
            int(self.f_3068946584496572486),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 14
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x14
        (
            self.f_1734190238197517228,
            self.f_3392370045775382312,
            self.f_6214993069921897693,
            self.f_510303099668681797,
            self.f_1276250833917656531,
            self.f_3068946584496572486,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_9152920230794971550(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_9152920230794971550().fields(\n'
        res += '\tf_3068946584496572486 = %s ,\n' % str(
            self.f_3068946584496572486)
        res += '\tf_1276250833917656531 = %s ,\n' % str(
            self.f_1276250833917656531)
        res += '\tf_510303099668681797 = %s ,\n' % str(
            self.f_510303099668681797)
        res += '\tf_6214993069921897693 = %s ,\n' % str(
            self.f_6214993069921897693)
        res += '\tf_3392370045775382312 = %s ,\n' % str(
            self.f_3392370045775382312)
        res += '\tf_1734190238197517228 = %s ,\n' % str(
            self.f_1734190238197517228)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 14

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_3068946584496572486(self):
        return self.__f_3068946584496572486

    def __set_f_3068946584496572486(self, value):

        assert (isinstance(value, (int, ADDR)))
        self.__f_3068946584496572486 = value if isinstance(
            value, ADDR) else ADDR(value)

    def __get_f_1276250833917656531(self):
        return self.__f_1276250833917656531

    def __set_f_1276250833917656531(self, value):

        assert (isinstance(value, (int, ADDR)))
        self.__f_1276250833917656531 = value if isinstance(
            value, ADDR) else ADDR(value)

    def __get_f_510303099668681797(self):
        return self.__f_510303099668681797

    def __set_f_510303099668681797(self, value):

        assert (isinstance(value, (int, ADDR)))
        self.__f_510303099668681797 = value if isinstance(value,
                                                          ADDR) else ADDR(value)

    def __get_f_6214993069921897693(self):
        return self.__f_6214993069921897693

    def __set_f_6214993069921897693(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_6214993069921897693 = int(value)

    def __get_f_3392370045775382312(self):
        return self.__f_3392370045775382312

    def __set_f_3392370045775382312(self, value):

        assert (isinstance(value, (int, SPARSIFIED)))
        self.__f_3392370045775382312 = value if isinstance(
            value, SPARSIFIED) else SPARSIFIED(value)

    def __get_f_1734190238197517228(self):
        return self.__f_1734190238197517228

    def __set_f_1734190238197517228(self, value):

        assert (isinstance(value, (int, COMPRESSED)))
        self.__f_1734190238197517228 = value if isinstance(
            value, COMPRESSED) else COMPRESSED(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_3068946584496572486 = property(__get_f_3068946584496572486,
                                     __set_f_3068946584496572486)
    f_1276250833917656531 = property(__get_f_1276250833917656531,
                                     __set_f_1276250833917656531)
    f_510303099668681797 = property(__get_f_510303099668681797,
                                    __set_f_510303099668681797)
    f_6214993069921897693 = property(__get_f_6214993069921897693,
                                     __set_f_6214993069921897693)
    f_3392370045775382312 = property(__get_f_3392370045775382312,
                                     __set_f_3392370045775382312)
    f_1734190238197517228 = property(__get_f_1734190238197517228,
                                     __set_f_1734190238197517228)


class inst_i_7204637145564182256(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_3068946584496572486: [ADDR, 32]  # type: ignore
    __f_1276250833917656531: [ADDR, 32]  # type: ignore
    __f_3392370045775382312: [SPARSIFIED, 1]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[ADDR, ADDR, SPARSIFIED,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(7)

        self.__f_3392370045775382312 = SPARSIFIED(0)
        cf_str += '>u1'
        self.__f_1276250833917656531 = ADDR(0)
        cf_str += '>u32'
        self.__f_3068946584496572486 = ADDR(0)
        cf_str += '>u32'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(21)

    def fields(
        self,
        f_3068946584496572486: ADDR = None,
        f_1276250833917656531: ADDR = None,
        f_3392370045775382312: SPARSIFIED = None,
    ):
        if f_3068946584496572486:
            self.f_3068946584496572486 = f_3068946584496572486
        if f_1276250833917656531:
            self.f_1276250833917656531 = f_1276250833917656531
        if f_3392370045775382312:
            self.f_3392370045775382312 = f_3392370045775382312
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_3392370045775382312),
            int(self.f_1276250833917656531),
            int(self.f_3068946584496572486),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 10
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x15
        (
            self.f_3392370045775382312,
            self.f_1276250833917656531,
            self.f_3068946584496572486,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_7204637145564182256(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_7204637145564182256().fields(\n'
        res += '\tf_3068946584496572486 = %s ,\n' % str(
            self.f_3068946584496572486)
        res += '\tf_1276250833917656531 = %s ,\n' % str(
            self.f_1276250833917656531)
        res += '\tf_3392370045775382312 = %s ,\n' % str(
            self.f_3392370045775382312)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 10

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_3068946584496572486(self):
        return self.__f_3068946584496572486

    def __set_f_3068946584496572486(self, value):

        assert (isinstance(value, (int, ADDR)))
        self.__f_3068946584496572486 = value if isinstance(
            value, ADDR) else ADDR(value)

    def __get_f_1276250833917656531(self):
        return self.__f_1276250833917656531

    def __set_f_1276250833917656531(self, value):

        assert (isinstance(value, (int, ADDR)))
        self.__f_1276250833917656531 = value if isinstance(
            value, ADDR) else ADDR(value)

    def __get_f_3392370045775382312(self):
        return self.__f_3392370045775382312

    def __set_f_3392370045775382312(self, value):

        assert (isinstance(value, (int, SPARSIFIED)))
        self.__f_3392370045775382312 = value if isinstance(
            value, SPARSIFIED) else SPARSIFIED(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_3068946584496572486 = property(__get_f_3068946584496572486,
                                     __set_f_3068946584496572486)
    f_1276250833917656531 = property(__get_f_1276250833917656531,
                                     __set_f_1276250833917656531)
    f_3392370045775382312 = property(__get_f_3392370045775382312,
                                     __set_f_3392370045775382312)


class inst_i_2089276022054688120(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_6920772091196212887: [CCRCLR, 8]  # type: ignore
    __f_1885779890895099474: [CCRCLR, 8]  # type: ignore
    __f_1851582658599760477: [CCRSET, 11]  # type: ignore
    __f_4535149732094779661: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_581203445514181141: [ADDR, 32]  # type: ignore
    __f_3913792219024292053: [PRECISION, 2]  # type: ignore
    __f_6532188106183563848: [PRECISION_DDR, 3]  # type: ignore
    __f_1770559390771253019: [QUAN_SIGNED, 1]  # type: ignore
    __f_8504158210894135380: [int, 21]  # type: ignore
    __f_6766582184502734391: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_967006719681078271: [datatype.uint16, 16]  # type: ignore
    __f_8538332288708448876: [datatype.uint16, 16]  # type: ignore
    __f_2801579247376141750: [datatype.uint16, 16]  # type: ignore
    __f_1205923120156011729: [datatype.uint16, 16]  # type: ignore
    __f_816100931824639168: [int, 2]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, CCRCLR, CCRSET, ADDR_GLB_8_WITH_BANK,
                               ADDR, PRECISION, PRECISION_DDR, QUAN_SIGNED, int,
                               ADDR_GLB_8_WITH_BANK, int, int, int, int,
                               int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(6)

        self.__f_816100931824639168 = int(0)
        cf_str += '>u2'
        self.__f_1205923120156011729 = int(0)
        cf_str += '>u16'
        self.__f_2801579247376141750 = int(0)
        cf_str += '>u16'
        self.__f_8538332288708448876 = int(0)
        cf_str += '>u16'
        self.__f_967006719681078271 = int(0)
        cf_str += '>u16'
        self.__f_6766582184502734391 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_8504158210894135380 = int(0)
        cf_str += '>u21'
        self.__f_1770559390771253019 = QUAN_SIGNED(0)
        cf_str += '>u1'
        self.__f_6532188106183563848 = PRECISION_DDR(0)
        cf_str += '>u3'
        self.__f_3913792219024292053 = PRECISION(0)
        cf_str += '>u2'
        self.__f_581203445514181141 = ADDR(0)
        cf_str += '>u32'
        self.__f_4535149732094779661 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_1851582658599760477 = CCRSET(0)
        cf_str += '>u11'
        self.__f_1885779890895099474 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_6920772091196212887 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(32)

    def fields(
        self,
        f_6920772091196212887: CCRCLR = None,
        f_1885779890895099474: CCRCLR = None,
        f_1851582658599760477: CCRSET = None,
        f_4535149732094779661: ADDR_GLB_8_WITH_BANK = None,
        f_581203445514181141: ADDR = None,
        f_3913792219024292053: PRECISION = None,
        f_6532188106183563848: PRECISION_DDR = None,
        f_1770559390771253019: QUAN_SIGNED = None,
        f_8504158210894135380: int = None,
        f_6766582184502734391: ADDR_GLB_8_WITH_BANK = None,
        f_967006719681078271: int = None,
        f_8538332288708448876: int = None,
        f_2801579247376141750: int = None,
        f_1205923120156011729: int = None,
        f_816100931824639168: int = None,
    ):
        if f_6920772091196212887:
            self.f_6920772091196212887 = f_6920772091196212887
        if f_1885779890895099474:
            self.f_1885779890895099474 = f_1885779890895099474
        if f_1851582658599760477:
            self.f_1851582658599760477 = f_1851582658599760477
        if f_4535149732094779661:
            self.f_4535149732094779661 = f_4535149732094779661
        if f_581203445514181141:
            self.f_581203445514181141 = f_581203445514181141
        if f_3913792219024292053:
            self.f_3913792219024292053 = f_3913792219024292053
        if f_6532188106183563848:
            self.f_6532188106183563848 = f_6532188106183563848
        if f_1770559390771253019:
            self.f_1770559390771253019 = f_1770559390771253019
        if f_8504158210894135380:
            self.f_8504158210894135380 = f_8504158210894135380
        if f_6766582184502734391:
            self.f_6766582184502734391 = f_6766582184502734391
        if f_967006719681078271:
            self.f_967006719681078271 = f_967006719681078271
        if f_8538332288708448876:
            self.f_8538332288708448876 = f_8538332288708448876
        if f_2801579247376141750:
            self.f_2801579247376141750 = f_2801579247376141750
        if f_1205923120156011729:
            self.f_1205923120156011729 = f_1205923120156011729
        if f_816100931824639168:
            self.f_816100931824639168 = f_816100931824639168
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_816100931824639168),
            int(self.f_1205923120156011729),
            int(self.f_2801579247376141750),
            int(self.f_8538332288708448876),
            int(self.f_967006719681078271),
            int(self.f_6766582184502734391),
            int(self.f_8504158210894135380),
            int(self.f_1770559390771253019),
            int(self.f_6532188106183563848),
            int(self.f_3913792219024292053),
            int(self.f_581203445514181141),
            int(self.f_4535149732094779661),
            int(self.f_1851582658599760477),
            int(self.f_1885779890895099474),
            int(self.f_6920772091196212887),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 27
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x20
        (
            self.f_816100931824639168,
            self.f_1205923120156011729,
            self.f_2801579247376141750,
            self.f_8538332288708448876,
            self.f_967006719681078271,
            self.f_6766582184502734391,
            self.f_8504158210894135380,
            self.f_1770559390771253019,
            self.f_6532188106183563848,
            self.f_3913792219024292053,
            self.f_581203445514181141,
            self.f_4535149732094779661,
            self.f_1851582658599760477,
            self.f_1885779890895099474,
            self.f_6920772091196212887,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_2089276022054688120(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_2089276022054688120().fields(\n'
        res += '\tf_6920772091196212887 = %s ,\n' % str(
            self.f_6920772091196212887)
        res += '\tf_1885779890895099474 = %s ,\n' % str(
            self.f_1885779890895099474)
        res += '\tf_1851582658599760477 = %s ,\n' % str(
            self.f_1851582658599760477)
        res += '\tf_4535149732094779661 = %s ,\n' % str(
            self.f_4535149732094779661)
        res += '\tf_581203445514181141 = %s ,\n' % str(
            self.f_581203445514181141)
        res += '\tf_3913792219024292053 = %s ,\n' % str(
            self.f_3913792219024292053)
        res += '\tf_6532188106183563848 = %s ,\n' % str(
            self.f_6532188106183563848)
        res += '\tf_1770559390771253019 = %s ,\n' % str(
            self.f_1770559390771253019)
        res += '\tf_8504158210894135380 = %s ,\n' % str(
            self.f_8504158210894135380)
        res += '\tf_6766582184502734391 = %s ,\n' % str(
            self.f_6766582184502734391)
        res += '\tf_967006719681078271 = %s ,\n' % str(
            self.f_967006719681078271)
        res += '\tf_8538332288708448876 = %s ,\n' % str(
            self.f_8538332288708448876)
        res += '\tf_2801579247376141750 = %s ,\n' % str(
            self.f_2801579247376141750)
        res += '\tf_1205923120156011729 = %s ,\n' % str(
            self.f_1205923120156011729)
        res += '\tf_816100931824639168 = %s ,\n' % str(
            self.f_816100931824639168)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 27

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_6920772091196212887(self):
        return self.__f_6920772091196212887

    def __set_f_6920772091196212887(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_6920772091196212887 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1885779890895099474(self):
        return self.__f_1885779890895099474

    def __set_f_1885779890895099474(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_1885779890895099474 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1851582658599760477(self):
        return self.__f_1851582658599760477

    def __set_f_1851582658599760477(self, value):

        assert (isinstance(value, (int, CCRSET)))
        self.__f_1851582658599760477 = value if isinstance(
            value, CCRSET) else CCRSET(value)

    def __get_f_4535149732094779661(self):
        return self.__f_4535149732094779661

    def __set_f_4535149732094779661(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_4535149732094779661 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_581203445514181141(self):
        return self.__f_581203445514181141

    def __set_f_581203445514181141(self, value):

        assert (isinstance(value, (int, ADDR)))
        self.__f_581203445514181141 = value if isinstance(value,
                                                          ADDR) else ADDR(value)

    def __get_f_3913792219024292053(self):
        return self.__f_3913792219024292053

    def __set_f_3913792219024292053(self, value):

        assert (isinstance(value, (int, PRECISION)))
        self.__f_3913792219024292053 = value if isinstance(
            value, PRECISION) else PRECISION(value)

    def __get_f_6532188106183563848(self):
        return self.__f_6532188106183563848

    def __set_f_6532188106183563848(self, value):

        assert (isinstance(value, (int, PRECISION_DDR)))
        self.__f_6532188106183563848 = value if isinstance(
            value, PRECISION_DDR) else PRECISION_DDR(value)

    def __get_f_1770559390771253019(self):
        return self.__f_1770559390771253019

    def __set_f_1770559390771253019(self, value):

        assert (isinstance(value, (int, QUAN_SIGNED)))
        self.__f_1770559390771253019 = value if isinstance(
            value, QUAN_SIGNED) else QUAN_SIGNED(value)

    def __get_f_8504158210894135380(self):
        return self.__f_8504158210894135380

    def __set_f_8504158210894135380(self, value):
        assert int(value) < 2**21

        assert int(value) >= 0

        self.__f_8504158210894135380 = int(value)

    def __get_f_6766582184502734391(self):
        return self.__f_6766582184502734391

    def __set_f_6766582184502734391(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_6766582184502734391 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_967006719681078271(self):
        return self.__f_967006719681078271

    def __set_f_967006719681078271(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_967006719681078271 = int(value)

    def __get_f_8538332288708448876(self):
        return self.__f_8538332288708448876

    def __set_f_8538332288708448876(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8538332288708448876 = int(value)

    def __get_f_2801579247376141750(self):
        return self.__f_2801579247376141750

    def __set_f_2801579247376141750(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_2801579247376141750 = int(value)

    def __get_f_1205923120156011729(self):
        return self.__f_1205923120156011729

    def __set_f_1205923120156011729(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1205923120156011729 = int(value)

    def __get_f_816100931824639168(self):
        return self.__f_816100931824639168

    def __set_f_816100931824639168(self, value):
        assert int(value) < 2**2

        assert int(value) >= 0

        self.__f_816100931824639168 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_6920772091196212887 = property(__get_f_6920772091196212887,
                                     __set_f_6920772091196212887)
    f_1885779890895099474 = property(__get_f_1885779890895099474,
                                     __set_f_1885779890895099474)
    f_1851582658599760477 = property(__get_f_1851582658599760477,
                                     __set_f_1851582658599760477)
    f_4535149732094779661 = property(__get_f_4535149732094779661,
                                     __set_f_4535149732094779661)
    f_581203445514181141 = property(__get_f_581203445514181141,
                                    __set_f_581203445514181141)
    f_3913792219024292053 = property(__get_f_3913792219024292053,
                                     __set_f_3913792219024292053)
    f_6532188106183563848 = property(__get_f_6532188106183563848,
                                     __set_f_6532188106183563848)
    f_1770559390771253019 = property(__get_f_1770559390771253019,
                                     __set_f_1770559390771253019)
    f_8504158210894135380 = property(__get_f_8504158210894135380,
                                     __set_f_8504158210894135380)
    f_6766582184502734391 = property(__get_f_6766582184502734391,
                                     __set_f_6766582184502734391)
    f_967006719681078271 = property(__get_f_967006719681078271,
                                    __set_f_967006719681078271)
    f_8538332288708448876 = property(__get_f_8538332288708448876,
                                     __set_f_8538332288708448876)
    f_2801579247376141750 = property(__get_f_2801579247376141750,
                                     __set_f_2801579247376141750)
    f_1205923120156011729 = property(__get_f_1205923120156011729,
                                     __set_f_1205923120156011729)
    f_816100931824639168 = property(__get_f_816100931824639168,
                                    __set_f_816100931824639168)


class inst_i_2841594760846416640(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_8522342661322622465: [datatype.uint16, 16]  # type: ignore
    __f_3676797385440794520: [datatype.uint16, 16]  # type: ignore
    __f_1654969283327896294: [datatype.uint16, 16]  # type: ignore
    __f_860775722809473967: [datatype.uint16, 16]  # type: ignore
    __f_1218174442252260153: [STRIDE_GLB, 64]  # type: ignore
    __f_2112052519892767027: [int, 4]  # type: ignore
    __f_6766582184502734391: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_1770559390771253019: [QUAN_SIGNED, 1]  # type: ignore
    __f_3913792219024292053: [PRECISION, 2]  # type: ignore
    __f_6532188106183563848: [PRECISION_DDR, 3]  # type: ignore
    __f_8617447463546780470: [QUAN_TYPE, 1]  # type: ignore
    __f_2801579247376141750: [datatype.uint16, 16]  # type: ignore
    __f_1205923120156011729: [datatype.uint16, 16]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int, int, int, int, STRIDE_GLB, int,
                               ADDR_GLB_8_WITH_BANK, QUAN_SIGNED, PRECISION,
                               PRECISION_DDR, QUAN_TYPE, int, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(4)

        self.__f_1205923120156011729 = int(0)
        cf_str += '>u16'
        self.__f_2801579247376141750 = int(0)
        cf_str += '>u16'
        self.__f_8617447463546780470 = QUAN_TYPE(0)
        cf_str += '>u1'
        self.__f_6532188106183563848 = PRECISION_DDR(0)
        cf_str += '>u3'
        self.__f_3913792219024292053 = PRECISION(0)
        cf_str += '>u2'
        self.__f_1770559390771253019 = QUAN_SIGNED(0)
        cf_str += '>u1'
        self.__f_6766582184502734391 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_2112052519892767027 = int(0)
        cf_str += '>u4'
        self.__f_1218174442252260153 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_860775722809473967 = int(0)
        cf_str += '>u16'
        self.__f_1654969283327896294 = int(0)
        cf_str += '>u16'
        self.__f_3676797385440794520 = int(0)
        cf_str += '>u16'
        self.__f_8522342661322622465 = int(0)
        cf_str += '>u16'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(33)

    def fields(
        self,
        f_8522342661322622465: int = None,
        f_3676797385440794520: int = None,
        f_1654969283327896294: int = None,
        f_860775722809473967: int = None,
        f_1218174442252260153: STRIDE_GLB = None,
        f_2112052519892767027: int = None,
        f_6766582184502734391: ADDR_GLB_8_WITH_BANK = None,
        f_1770559390771253019: QUAN_SIGNED = None,
        f_3913792219024292053: PRECISION = None,
        f_6532188106183563848: PRECISION_DDR = None,
        f_8617447463546780470: QUAN_TYPE = None,
        f_2801579247376141750: int = None,
        f_1205923120156011729: int = None,
    ):
        if f_8522342661322622465:
            self.f_8522342661322622465 = f_8522342661322622465
        if f_3676797385440794520:
            self.f_3676797385440794520 = f_3676797385440794520
        if f_1654969283327896294:
            self.f_1654969283327896294 = f_1654969283327896294
        if f_860775722809473967:
            self.f_860775722809473967 = f_860775722809473967
        if f_1218174442252260153:
            self.f_1218174442252260153 = f_1218174442252260153
        if f_2112052519892767027:
            self.f_2112052519892767027 = f_2112052519892767027
        if f_6766582184502734391:
            self.f_6766582184502734391 = f_6766582184502734391
        if f_1770559390771253019:
            self.f_1770559390771253019 = f_1770559390771253019
        if f_3913792219024292053:
            self.f_3913792219024292053 = f_3913792219024292053
        if f_6532188106183563848:
            self.f_6532188106183563848 = f_6532188106183563848
        if f_8617447463546780470:
            self.f_8617447463546780470 = f_8617447463546780470
        if f_2801579247376141750:
            self.f_2801579247376141750 = f_2801579247376141750
        if f_1205923120156011729:
            self.f_1205923120156011729 = f_1205923120156011729
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_1205923120156011729),
            int(self.f_2801579247376141750),
            int(self.f_8617447463546780470),
            int(self.f_6532188106183563848),
            int(self.f_3913792219024292053),
            int(self.f_1770559390771253019),
            int(self.f_6766582184502734391),
            int(self.f_2112052519892767027),
            int(self.f_1218174442252260153),
            int(self.f_860775722809473967),
            int(self.f_1654969283327896294),
            int(self.f_3676797385440794520),
            int(self.f_8522342661322622465),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 26
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x21
        (
            self.f_1205923120156011729,
            self.f_2801579247376141750,
            self.f_8617447463546780470,
            self.f_6532188106183563848,
            self.f_3913792219024292053,
            self.f_1770559390771253019,
            self.f_6766582184502734391,
            self.f_2112052519892767027,
            self.f_1218174442252260153,
            self.f_860775722809473967,
            self.f_1654969283327896294,
            self.f_3676797385440794520,
            self.f_8522342661322622465,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_2841594760846416640(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_2841594760846416640().fields(\n'
        res += '\tf_8522342661322622465 = %s ,\n' % str(
            self.f_8522342661322622465)
        res += '\tf_3676797385440794520 = %s ,\n' % str(
            self.f_3676797385440794520)
        res += '\tf_1654969283327896294 = %s ,\n' % str(
            self.f_1654969283327896294)
        res += '\tf_860775722809473967 = %s ,\n' % str(
            self.f_860775722809473967)
        res += '\tf_1218174442252260153 = %s ,\n' % str(
            self.f_1218174442252260153)
        res += '\tf_2112052519892767027 = %s ,\n' % str(
            self.f_2112052519892767027)
        res += '\tf_6766582184502734391 = %s ,\n' % str(
            self.f_6766582184502734391)
        res += '\tf_1770559390771253019 = %s ,\n' % str(
            self.f_1770559390771253019)
        res += '\tf_3913792219024292053 = %s ,\n' % str(
            self.f_3913792219024292053)
        res += '\tf_6532188106183563848 = %s ,\n' % str(
            self.f_6532188106183563848)
        res += '\tf_8617447463546780470 = %s ,\n' % str(
            self.f_8617447463546780470)
        res += '\tf_2801579247376141750 = %s ,\n' % str(
            self.f_2801579247376141750)
        res += '\tf_1205923120156011729 = %s ,\n' % str(
            self.f_1205923120156011729)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 26

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_8522342661322622465(self):
        return self.__f_8522342661322622465

    def __set_f_8522342661322622465(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8522342661322622465 = int(value)

    def __get_f_3676797385440794520(self):
        return self.__f_3676797385440794520

    def __set_f_3676797385440794520(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_3676797385440794520 = int(value)

    def __get_f_1654969283327896294(self):
        return self.__f_1654969283327896294

    def __set_f_1654969283327896294(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1654969283327896294 = int(value)

    def __get_f_860775722809473967(self):
        return self.__f_860775722809473967

    def __set_f_860775722809473967(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_860775722809473967 = int(value)

    def __get_f_1218174442252260153(self):
        return self.__f_1218174442252260153

    def __set_f_1218174442252260153(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_1218174442252260153 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_2112052519892767027(self):
        return self.__f_2112052519892767027

    def __set_f_2112052519892767027(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_2112052519892767027 = int(value)

    def __get_f_6766582184502734391(self):
        return self.__f_6766582184502734391

    def __set_f_6766582184502734391(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_6766582184502734391 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_1770559390771253019(self):
        return self.__f_1770559390771253019

    def __set_f_1770559390771253019(self, value):

        assert (isinstance(value, (int, QUAN_SIGNED)))
        self.__f_1770559390771253019 = value if isinstance(
            value, QUAN_SIGNED) else QUAN_SIGNED(value)

    def __get_f_3913792219024292053(self):
        return self.__f_3913792219024292053

    def __set_f_3913792219024292053(self, value):

        assert (isinstance(value, (int, PRECISION)))
        self.__f_3913792219024292053 = value if isinstance(
            value, PRECISION) else PRECISION(value)

    def __get_f_6532188106183563848(self):
        return self.__f_6532188106183563848

    def __set_f_6532188106183563848(self, value):

        assert (isinstance(value, (int, PRECISION_DDR)))
        self.__f_6532188106183563848 = value if isinstance(
            value, PRECISION_DDR) else PRECISION_DDR(value)

    def __get_f_8617447463546780470(self):
        return self.__f_8617447463546780470

    def __set_f_8617447463546780470(self, value):

        assert (isinstance(value, (int, QUAN_TYPE)))
        self.__f_8617447463546780470 = value if isinstance(
            value, QUAN_TYPE) else QUAN_TYPE(value)

    def __get_f_2801579247376141750(self):
        return self.__f_2801579247376141750

    def __set_f_2801579247376141750(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_2801579247376141750 = int(value)

    def __get_f_1205923120156011729(self):
        return self.__f_1205923120156011729

    def __set_f_1205923120156011729(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1205923120156011729 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_8522342661322622465 = property(__get_f_8522342661322622465,
                                     __set_f_8522342661322622465)
    f_3676797385440794520 = property(__get_f_3676797385440794520,
                                     __set_f_3676797385440794520)
    f_1654969283327896294 = property(__get_f_1654969283327896294,
                                     __set_f_1654969283327896294)
    f_860775722809473967 = property(__get_f_860775722809473967,
                                    __set_f_860775722809473967)
    f_1218174442252260153 = property(__get_f_1218174442252260153,
                                     __set_f_1218174442252260153)
    f_2112052519892767027 = property(__get_f_2112052519892767027,
                                     __set_f_2112052519892767027)
    f_6766582184502734391 = property(__get_f_6766582184502734391,
                                     __set_f_6766582184502734391)
    f_1770559390771253019 = property(__get_f_1770559390771253019,
                                     __set_f_1770559390771253019)
    f_3913792219024292053 = property(__get_f_3913792219024292053,
                                     __set_f_3913792219024292053)
    f_6532188106183563848 = property(__get_f_6532188106183563848,
                                     __set_f_6532188106183563848)
    f_8617447463546780470 = property(__get_f_8617447463546780470,
                                     __set_f_8617447463546780470)
    f_2801579247376141750 = property(__get_f_2801579247376141750,
                                     __set_f_2801579247376141750)
    f_1205923120156011729 = property(__get_f_1205923120156011729,
                                     __set_f_1205923120156011729)


class inst_i_3414519735293012969(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_6920772091196212887: [CCRCLR, 8]  # type: ignore
    __f_1885779890895099474: [CCRCLR, 8]  # type: ignore
    __f_1851582658599760477: [CCRSET, 11]  # type: ignore
    __f_4535149732094779661: [ADDR_GLB_8_WITHOUT_BANK, 21]  # type: ignore
    __f_581203445514181141: [ADDR, 32]  # type: ignore
    __f_1449988654089269400: [datatype.uint16, 16]  # type: ignore
    __f_8538332288708448876: [datatype.uint16, 16]  # type: ignore
    __f_8660001712953173509: [datatype.uint16, 16]  # type: ignore
    __f_2401380060870497267: [datatype.uint16, 16]  # type: ignore
    __f_816100931824639168: [int, 2]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, CCRCLR, CCRSET, ADDR_GLB_8_WITHOUT_BANK,
                               ADDR, int, int, int, int, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(6)

        self.__f_816100931824639168 = int(0)
        cf_str += '>u2'
        self.__f_2401380060870497267 = int(0)
        cf_str += '>u16'
        self.__f_8660001712953173509 = int(0)
        cf_str += '>u16'
        self.__f_8538332288708448876 = int(0)
        cf_str += '>u16'
        self.__f_1449988654089269400 = int(0)
        cf_str += '>u16'
        self.__f_581203445514181141 = ADDR(0)
        cf_str += '>u32'
        self.__f_4535149732094779661 = ADDR_GLB_8_WITHOUT_BANK(0)
        cf_str += '>u21'
        self.__f_1851582658599760477 = CCRSET(0)
        cf_str += '>u11'
        self.__f_1885779890895099474 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_6920772091196212887 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(34)

    def fields(
        self,
        f_6920772091196212887: CCRCLR = None,
        f_1885779890895099474: CCRCLR = None,
        f_1851582658599760477: CCRSET = None,
        f_4535149732094779661: ADDR_GLB_8_WITHOUT_BANK = None,
        f_581203445514181141: ADDR = None,
        f_1449988654089269400: int = None,
        f_8538332288708448876: int = None,
        f_8660001712953173509: int = None,
        f_2401380060870497267: int = None,
        f_816100931824639168: int = None,
    ):
        if f_6920772091196212887:
            self.f_6920772091196212887 = f_6920772091196212887
        if f_1885779890895099474:
            self.f_1885779890895099474 = f_1885779890895099474
        if f_1851582658599760477:
            self.f_1851582658599760477 = f_1851582658599760477
        if f_4535149732094779661:
            self.f_4535149732094779661 = f_4535149732094779661
        if f_581203445514181141:
            self.f_581203445514181141 = f_581203445514181141
        if f_1449988654089269400:
            self.f_1449988654089269400 = f_1449988654089269400
        if f_8538332288708448876:
            self.f_8538332288708448876 = f_8538332288708448876
        if f_8660001712953173509:
            self.f_8660001712953173509 = f_8660001712953173509
        if f_2401380060870497267:
            self.f_2401380060870497267 = f_2401380060870497267
        if f_816100931824639168:
            self.f_816100931824639168 = f_816100931824639168
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_816100931824639168),
            int(self.f_2401380060870497267),
            int(self.f_8660001712953173509),
            int(self.f_8538332288708448876),
            int(self.f_1449988654089269400),
            int(self.f_581203445514181141),
            int(self.f_4535149732094779661),
            int(self.f_1851582658599760477),
            int(self.f_1885779890895099474),
            int(self.f_6920772091196212887),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 20
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x22
        (
            self.f_816100931824639168,
            self.f_2401380060870497267,
            self.f_8660001712953173509,
            self.f_8538332288708448876,
            self.f_1449988654089269400,
            self.f_581203445514181141,
            self.f_4535149732094779661,
            self.f_1851582658599760477,
            self.f_1885779890895099474,
            self.f_6920772091196212887,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_3414519735293012969(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_3414519735293012969().fields(\n'
        res += '\tf_6920772091196212887 = %s ,\n' % str(
            self.f_6920772091196212887)
        res += '\tf_1885779890895099474 = %s ,\n' % str(
            self.f_1885779890895099474)
        res += '\tf_1851582658599760477 = %s ,\n' % str(
            self.f_1851582658599760477)
        res += '\tf_4535149732094779661 = %s ,\n' % str(
            self.f_4535149732094779661)
        res += '\tf_581203445514181141 = %s ,\n' % str(
            self.f_581203445514181141)
        res += '\tf_1449988654089269400 = %s ,\n' % str(
            self.f_1449988654089269400)
        res += '\tf_8538332288708448876 = %s ,\n' % str(
            self.f_8538332288708448876)
        res += '\tf_8660001712953173509 = %s ,\n' % str(
            self.f_8660001712953173509)
        res += '\tf_2401380060870497267 = %s ,\n' % str(
            self.f_2401380060870497267)
        res += '\tf_816100931824639168 = %s ,\n' % str(
            self.f_816100931824639168)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 20

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_6920772091196212887(self):
        return self.__f_6920772091196212887

    def __set_f_6920772091196212887(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_6920772091196212887 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1885779890895099474(self):
        return self.__f_1885779890895099474

    def __set_f_1885779890895099474(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_1885779890895099474 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1851582658599760477(self):
        return self.__f_1851582658599760477

    def __set_f_1851582658599760477(self, value):

        assert (isinstance(value, (int, CCRSET)))
        self.__f_1851582658599760477 = value if isinstance(
            value, CCRSET) else CCRSET(value)

    def __get_f_4535149732094779661(self):
        return self.__f_4535149732094779661

    def __set_f_4535149732094779661(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITHOUT_BANK)))
        self.__f_4535149732094779661 = value if isinstance(
            value, ADDR_GLB_8_WITHOUT_BANK) else ADDR_GLB_8_WITHOUT_BANK(value)

    def __get_f_581203445514181141(self):
        return self.__f_581203445514181141

    def __set_f_581203445514181141(self, value):

        assert (isinstance(value, (int, ADDR)))
        self.__f_581203445514181141 = value if isinstance(value,
                                                          ADDR) else ADDR(value)

    def __get_f_1449988654089269400(self):
        return self.__f_1449988654089269400

    def __set_f_1449988654089269400(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1449988654089269400 = int(value)

    def __get_f_8538332288708448876(self):
        return self.__f_8538332288708448876

    def __set_f_8538332288708448876(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8538332288708448876 = int(value)

    def __get_f_8660001712953173509(self):
        return self.__f_8660001712953173509

    def __set_f_8660001712953173509(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8660001712953173509 = int(value)

    def __get_f_2401380060870497267(self):
        return self.__f_2401380060870497267

    def __set_f_2401380060870497267(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_2401380060870497267 = int(value)

    def __get_f_816100931824639168(self):
        return self.__f_816100931824639168

    def __set_f_816100931824639168(self, value):
        assert int(value) < 2**2

        assert int(value) >= 0

        self.__f_816100931824639168 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_6920772091196212887 = property(__get_f_6920772091196212887,
                                     __set_f_6920772091196212887)
    f_1885779890895099474 = property(__get_f_1885779890895099474,
                                     __set_f_1885779890895099474)
    f_1851582658599760477 = property(__get_f_1851582658599760477,
                                     __set_f_1851582658599760477)
    f_4535149732094779661 = property(__get_f_4535149732094779661,
                                     __set_f_4535149732094779661)
    f_581203445514181141 = property(__get_f_581203445514181141,
                                    __set_f_581203445514181141)
    f_1449988654089269400 = property(__get_f_1449988654089269400,
                                     __set_f_1449988654089269400)
    f_8538332288708448876 = property(__get_f_8538332288708448876,
                                     __set_f_8538332288708448876)
    f_8660001712953173509 = property(__get_f_8660001712953173509,
                                     __set_f_8660001712953173509)
    f_2401380060870497267 = property(__get_f_2401380060870497267,
                                     __set_f_2401380060870497267)
    f_816100931824639168 = property(__get_f_816100931824639168,
                                    __set_f_816100931824639168)


class inst_i_3246495767012874974(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_3068946584496572486: [ADDR, 32]  # type: ignore
    __f_1276250833917656531: [ADDR, 32]  # type: ignore
    __f_510303099668681797: [ADDR, 32]  # type: ignore
    __f_6214993069921897693: [int, 4]  # type: ignore
    __f_3392370045775382312: [SPARSIFIED, 1]  # type: ignore
    __f_1734190238197517228: [COMPRESSED, 1]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[ADDR, ADDR, ADDR, int, SPARSIFIED,
                               COMPRESSED,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(2)

        self.__f_1734190238197517228 = COMPRESSED(0)
        cf_str += '>u1'
        self.__f_3392370045775382312 = SPARSIFIED(0)
        cf_str += '>u1'
        self.__f_6214993069921897693 = int(0)
        cf_str += '>u4'
        self.__f_510303099668681797 = ADDR(0)
        cf_str += '>u32'
        self.__f_1276250833917656531 = ADDR(0)
        cf_str += '>u32'
        self.__f_3068946584496572486 = ADDR(0)
        cf_str += '>u32'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(36)

    def fields(
        self,
        f_3068946584496572486: ADDR = None,
        f_1276250833917656531: ADDR = None,
        f_510303099668681797: ADDR = None,
        f_6214993069921897693: int = None,
        f_3392370045775382312: SPARSIFIED = None,
        f_1734190238197517228: COMPRESSED = None,
    ):
        if f_3068946584496572486:
            self.f_3068946584496572486 = f_3068946584496572486
        if f_1276250833917656531:
            self.f_1276250833917656531 = f_1276250833917656531
        if f_510303099668681797:
            self.f_510303099668681797 = f_510303099668681797
        if f_6214993069921897693:
            self.f_6214993069921897693 = f_6214993069921897693
        if f_3392370045775382312:
            self.f_3392370045775382312 = f_3392370045775382312
        if f_1734190238197517228:
            self.f_1734190238197517228 = f_1734190238197517228
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_1734190238197517228),
            int(self.f_3392370045775382312),
            int(self.f_6214993069921897693),
            int(self.f_510303099668681797),
            int(self.f_1276250833917656531),
            int(self.f_3068946584496572486),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 14
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x24
        (
            self.f_1734190238197517228,
            self.f_3392370045775382312,
            self.f_6214993069921897693,
            self.f_510303099668681797,
            self.f_1276250833917656531,
            self.f_3068946584496572486,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_3246495767012874974(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_3246495767012874974().fields(\n'
        res += '\tf_3068946584496572486 = %s ,\n' % str(
            self.f_3068946584496572486)
        res += '\tf_1276250833917656531 = %s ,\n' % str(
            self.f_1276250833917656531)
        res += '\tf_510303099668681797 = %s ,\n' % str(
            self.f_510303099668681797)
        res += '\tf_6214993069921897693 = %s ,\n' % str(
            self.f_6214993069921897693)
        res += '\tf_3392370045775382312 = %s ,\n' % str(
            self.f_3392370045775382312)
        res += '\tf_1734190238197517228 = %s ,\n' % str(
            self.f_1734190238197517228)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 14

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_3068946584496572486(self):
        return self.__f_3068946584496572486

    def __set_f_3068946584496572486(self, value):

        assert (isinstance(value, (int, ADDR)))
        self.__f_3068946584496572486 = value if isinstance(
            value, ADDR) else ADDR(value)

    def __get_f_1276250833917656531(self):
        return self.__f_1276250833917656531

    def __set_f_1276250833917656531(self, value):

        assert (isinstance(value, (int, ADDR)))
        self.__f_1276250833917656531 = value if isinstance(
            value, ADDR) else ADDR(value)

    def __get_f_510303099668681797(self):
        return self.__f_510303099668681797

    def __set_f_510303099668681797(self, value):

        assert (isinstance(value, (int, ADDR)))
        self.__f_510303099668681797 = value if isinstance(value,
                                                          ADDR) else ADDR(value)

    def __get_f_6214993069921897693(self):
        return self.__f_6214993069921897693

    def __set_f_6214993069921897693(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_6214993069921897693 = int(value)

    def __get_f_3392370045775382312(self):
        return self.__f_3392370045775382312

    def __set_f_3392370045775382312(self, value):

        assert (isinstance(value, (int, SPARSIFIED)))
        self.__f_3392370045775382312 = value if isinstance(
            value, SPARSIFIED) else SPARSIFIED(value)

    def __get_f_1734190238197517228(self):
        return self.__f_1734190238197517228

    def __set_f_1734190238197517228(self, value):

        assert (isinstance(value, (int, COMPRESSED)))
        self.__f_1734190238197517228 = value if isinstance(
            value, COMPRESSED) else COMPRESSED(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_3068946584496572486 = property(__get_f_3068946584496572486,
                                     __set_f_3068946584496572486)
    f_1276250833917656531 = property(__get_f_1276250833917656531,
                                     __set_f_1276250833917656531)
    f_510303099668681797 = property(__get_f_510303099668681797,
                                    __set_f_510303099668681797)
    f_6214993069921897693 = property(__get_f_6214993069921897693,
                                     __set_f_6214993069921897693)
    f_3392370045775382312 = property(__get_f_3392370045775382312,
                                     __set_f_3392370045775382312)
    f_1734190238197517228 = property(__get_f_1734190238197517228,
                                     __set_f_1734190238197517228)


class inst_i_8339684182387014894(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_3068946584496572486: [ADDR, 32]  # type: ignore
    __f_1276250833917656531: [ADDR, 32]  # type: ignore
    __f_3392370045775382312: [SPARSIFIED, 1]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[ADDR, ADDR, SPARSIFIED,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(7)

        self.__f_3392370045775382312 = SPARSIFIED(0)
        cf_str += '>u1'
        self.__f_1276250833917656531 = ADDR(0)
        cf_str += '>u32'
        self.__f_3068946584496572486 = ADDR(0)
        cf_str += '>u32'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(37)

    def fields(
        self,
        f_3068946584496572486: ADDR = None,
        f_1276250833917656531: ADDR = None,
        f_3392370045775382312: SPARSIFIED = None,
    ):
        if f_3068946584496572486:
            self.f_3068946584496572486 = f_3068946584496572486
        if f_1276250833917656531:
            self.f_1276250833917656531 = f_1276250833917656531
        if f_3392370045775382312:
            self.f_3392370045775382312 = f_3392370045775382312
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_3392370045775382312),
            int(self.f_1276250833917656531),
            int(self.f_3068946584496572486),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 10
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x25
        (
            self.f_3392370045775382312,
            self.f_1276250833917656531,
            self.f_3068946584496572486,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_8339684182387014894(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_8339684182387014894().fields(\n'
        res += '\tf_3068946584496572486 = %s ,\n' % str(
            self.f_3068946584496572486)
        res += '\tf_1276250833917656531 = %s ,\n' % str(
            self.f_1276250833917656531)
        res += '\tf_3392370045775382312 = %s ,\n' % str(
            self.f_3392370045775382312)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 10

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_3068946584496572486(self):
        return self.__f_3068946584496572486

    def __set_f_3068946584496572486(self, value):

        assert (isinstance(value, (int, ADDR)))
        self.__f_3068946584496572486 = value if isinstance(
            value, ADDR) else ADDR(value)

    def __get_f_1276250833917656531(self):
        return self.__f_1276250833917656531

    def __set_f_1276250833917656531(self, value):

        assert (isinstance(value, (int, ADDR)))
        self.__f_1276250833917656531 = value if isinstance(
            value, ADDR) else ADDR(value)

    def __get_f_3392370045775382312(self):
        return self.__f_3392370045775382312

    def __set_f_3392370045775382312(self, value):

        assert (isinstance(value, (int, SPARSIFIED)))
        self.__f_3392370045775382312 = value if isinstance(
            value, SPARSIFIED) else SPARSIFIED(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_3068946584496572486 = property(__get_f_3068946584496572486,
                                     __set_f_3068946584496572486)
    f_1276250833917656531 = property(__get_f_1276250833917656531,
                                     __set_f_1276250833917656531)
    f_3392370045775382312 = property(__get_f_3392370045775382312,
                                     __set_f_3392370045775382312)


class inst_i_6868657659093990379(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_5376608655877383655: [BROADCAST, 1]  # type: ignore
    __f_7602250604375468052: [BROADCAST, 1]  # type: ignore
    __f_299876935781518179: [int, 1]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[BROADCAST, BROADCAST, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(5)

        self.__f_299876935781518179 = int(0)
        cf_str += '>u1'
        self.__f_7602250604375468052 = BROADCAST(0)
        cf_str += '>u1'
        self.__f_5376608655877383655 = BROADCAST(0)
        cf_str += '>u1'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(65)

    def fields(
        self,
        f_5376608655877383655: BROADCAST = None,
        f_7602250604375468052: BROADCAST = None,
        f_299876935781518179: int = None,
    ):
        if f_5376608655877383655:
            self.f_5376608655877383655 = f_5376608655877383655
        if f_7602250604375468052:
            self.f_7602250604375468052 = f_7602250604375468052
        if f_299876935781518179:
            self.f_299876935781518179 = f_299876935781518179
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_299876935781518179),
            int(self.f_7602250604375468052),
            int(self.f_5376608655877383655),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 2
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x41
        (
            self.f_299876935781518179,
            self.f_7602250604375468052,
            self.f_5376608655877383655,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_6868657659093990379(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_6868657659093990379().fields(\n'
        res += '\tf_5376608655877383655 = %s ,\n' % str(
            self.f_5376608655877383655)
        res += '\tf_7602250604375468052 = %s ,\n' % str(
            self.f_7602250604375468052)
        res += '\tf_299876935781518179 = %s ,\n' % str(
            self.f_299876935781518179)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 2

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_5376608655877383655(self):
        return self.__f_5376608655877383655

    def __set_f_5376608655877383655(self, value):

        assert (isinstance(value, (int, BROADCAST)))
        self.__f_5376608655877383655 = value if isinstance(
            value, BROADCAST) else BROADCAST(value)

    def __get_f_7602250604375468052(self):
        return self.__f_7602250604375468052

    def __set_f_7602250604375468052(self, value):

        assert (isinstance(value, (int, BROADCAST)))
        self.__f_7602250604375468052 = value if isinstance(
            value, BROADCAST) else BROADCAST(value)

    def __get_f_299876935781518179(self):
        return self.__f_299876935781518179

    def __set_f_299876935781518179(self, value):
        assert int(value) < 2**1

        assert int(value) >= 0

        self.__f_299876935781518179 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_5376608655877383655 = property(__get_f_5376608655877383655,
                                     __set_f_5376608655877383655)
    f_7602250604375468052 = property(__get_f_7602250604375468052,
                                     __set_f_7602250604375468052)
    f_299876935781518179 = property(__get_f_299876935781518179,
                                    __set_f_299876935781518179)


class inst_i_8430774666881311866(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_8525072872364582718: [int, 4]  # type: ignore
    __f_9191315765263269885: [STRIDE_GLB, 64]  # type: ignore
    __f_1903538310092688587: [datatype.uint16, 16]  # type: ignore
    __f_2617505763564278546: [datatype.uint16, 16]  # type: ignore
    __f_6226735239301116980: [datatype.uint8, 8]  # type: ignore
    __f_668843506724768408: [datatype.uint8, 8]  # type: ignore
    __f_6402563436718652275: [datatype.uint8, 8]  # type: ignore
    __f_7097397218627294709: [datatype.uint8, 8]  # type: ignore
    __f_4207545581028892358: [int, 5]  # type: ignore
    __f_4739546102366045703: [datatype.uint8, 8]  # type: ignore
    __f_2824798772165075035: [int, 1]  # type: ignore
    __f_2112052519892767027: [int, 4]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int, STRIDE_GLB, int, int, int, int, int, int,
                               int, int, int, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(2)

        self.__f_2112052519892767027 = int(0)
        cf_str += '>u4'
        self.__f_2824798772165075035 = int(0)
        cf_str += '>u1'
        self.__f_4739546102366045703 = int(0)
        cf_str += '>u8'
        self.__f_4207545581028892358 = int(0)
        cf_str += '>u5'
        self.__f_7097397218627294709 = int(0)
        cf_str += '>u8'
        self.__f_6402563436718652275 = int(0)
        cf_str += '>u8'
        self.__f_668843506724768408 = int(0)
        cf_str += '>u8'
        self.__f_6226735239301116980 = int(0)
        cf_str += '>u8'
        self.__f_2617505763564278546 = int(0)
        cf_str += '>u16'
        self.__f_1903538310092688587 = int(0)
        cf_str += '>u16'
        self.__f_9191315765263269885 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_8525072872364582718 = int(0)
        cf_str += '>u4'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(66)

    def fields(
        self,
        f_8525072872364582718: int = None,
        f_9191315765263269885: STRIDE_GLB = None,
        f_1903538310092688587: int = None,
        f_2617505763564278546: int = None,
        f_6226735239301116980: int = None,
        f_668843506724768408: int = None,
        f_6402563436718652275: int = None,
        f_7097397218627294709: int = None,
        f_4207545581028892358: int = None,
        f_4739546102366045703: int = None,
        f_2824798772165075035: int = None,
        f_2112052519892767027: int = None,
    ):
        if f_8525072872364582718:
            self.f_8525072872364582718 = f_8525072872364582718
        if f_9191315765263269885:
            self.f_9191315765263269885 = f_9191315765263269885
        if f_1903538310092688587:
            self.f_1903538310092688587 = f_1903538310092688587
        if f_2617505763564278546:
            self.f_2617505763564278546 = f_2617505763564278546
        if f_6226735239301116980:
            self.f_6226735239301116980 = f_6226735239301116980
        if f_668843506724768408:
            self.f_668843506724768408 = f_668843506724768408
        if f_6402563436718652275:
            self.f_6402563436718652275 = f_6402563436718652275
        if f_7097397218627294709:
            self.f_7097397218627294709 = f_7097397218627294709
        if f_4207545581028892358:
            self.f_4207545581028892358 = f_4207545581028892358
        if f_4739546102366045703:
            self.f_4739546102366045703 = f_4739546102366045703
        if f_2824798772165075035:
            self.f_2824798772165075035 = f_2824798772165075035
        if f_2112052519892767027:
            self.f_2112052519892767027 = f_2112052519892767027
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_2112052519892767027),
            int(self.f_2824798772165075035),
            int(self.f_4739546102366045703),
            int(self.f_4207545581028892358),
            int(self.f_7097397218627294709),
            int(self.f_6402563436718652275),
            int(self.f_668843506724768408),
            int(self.f_6226735239301116980),
            int(self.f_2617505763564278546),
            int(self.f_1903538310092688587),
            int(self.f_9191315765263269885),
            int(self.f_8525072872364582718),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 20
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x42
        (
            self.f_2112052519892767027,
            self.f_2824798772165075035,
            self.f_4739546102366045703,
            self.f_4207545581028892358,
            self.f_7097397218627294709,
            self.f_6402563436718652275,
            self.f_668843506724768408,
            self.f_6226735239301116980,
            self.f_2617505763564278546,
            self.f_1903538310092688587,
            self.f_9191315765263269885,
            self.f_8525072872364582718,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_8430774666881311866(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_8430774666881311866().fields(\n'
        res += '\tf_8525072872364582718 = %s ,\n' % str(
            self.f_8525072872364582718)
        res += '\tf_9191315765263269885 = %s ,\n' % str(
            self.f_9191315765263269885)
        res += '\tf_1903538310092688587 = %s ,\n' % str(
            self.f_1903538310092688587)
        res += '\tf_2617505763564278546 = %s ,\n' % str(
            self.f_2617505763564278546)
        res += '\tf_6226735239301116980 = %s ,\n' % str(
            self.f_6226735239301116980)
        res += '\tf_668843506724768408 = %s ,\n' % str(
            self.f_668843506724768408)
        res += '\tf_6402563436718652275 = %s ,\n' % str(
            self.f_6402563436718652275)
        res += '\tf_7097397218627294709 = %s ,\n' % str(
            self.f_7097397218627294709)
        res += '\tf_4207545581028892358 = %s ,\n' % str(
            self.f_4207545581028892358)
        res += '\tf_4739546102366045703 = %s ,\n' % str(
            self.f_4739546102366045703)
        res += '\tf_2824798772165075035 = %s ,\n' % str(
            self.f_2824798772165075035)
        res += '\tf_2112052519892767027 = %s ,\n' % str(
            self.f_2112052519892767027)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 20

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_8525072872364582718(self):
        return self.__f_8525072872364582718

    def __set_f_8525072872364582718(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_8525072872364582718 = int(value)

    def __get_f_9191315765263269885(self):
        return self.__f_9191315765263269885

    def __set_f_9191315765263269885(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_9191315765263269885 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_1903538310092688587(self):
        return self.__f_1903538310092688587

    def __set_f_1903538310092688587(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1903538310092688587 = int(value)

    def __get_f_2617505763564278546(self):
        return self.__f_2617505763564278546

    def __set_f_2617505763564278546(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_2617505763564278546 = int(value)

    def __get_f_6226735239301116980(self):
        return self.__f_6226735239301116980

    def __set_f_6226735239301116980(self, value):
        assert int(value) < 2**8

        assert int(value) >= 0

        self.__f_6226735239301116980 = int(value)

    def __get_f_668843506724768408(self):
        return self.__f_668843506724768408

    def __set_f_668843506724768408(self, value):
        assert int(value) < 2**8

        assert int(value) >= 0

        self.__f_668843506724768408 = int(value)

    def __get_f_6402563436718652275(self):
        return self.__f_6402563436718652275

    def __set_f_6402563436718652275(self, value):
        assert int(value) < 2**8

        assert int(value) >= 0

        self.__f_6402563436718652275 = int(value)

    def __get_f_7097397218627294709(self):
        return self.__f_7097397218627294709

    def __set_f_7097397218627294709(self, value):
        assert int(value) < 2**8

        assert int(value) >= 0

        self.__f_7097397218627294709 = int(value)

    def __get_f_4207545581028892358(self):
        return self.__f_4207545581028892358

    def __set_f_4207545581028892358(self, value):
        assert int(value) < 2**5

        assert int(value) >= 0

        self.__f_4207545581028892358 = int(value)

    def __get_f_4739546102366045703(self):
        return self.__f_4739546102366045703

    def __set_f_4739546102366045703(self, value):
        assert int(value) < 2**8

        assert int(value) >= 0

        self.__f_4739546102366045703 = int(value)

    def __get_f_2824798772165075035(self):
        return self.__f_2824798772165075035

    def __set_f_2824798772165075035(self, value):
        assert int(value) < 2**1

        assert int(value) >= 0

        self.__f_2824798772165075035 = int(value)

    def __get_f_2112052519892767027(self):
        return self.__f_2112052519892767027

    def __set_f_2112052519892767027(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_2112052519892767027 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_8525072872364582718 = property(__get_f_8525072872364582718,
                                     __set_f_8525072872364582718)
    f_9191315765263269885 = property(__get_f_9191315765263269885,
                                     __set_f_9191315765263269885)
    f_1903538310092688587 = property(__get_f_1903538310092688587,
                                     __set_f_1903538310092688587)
    f_2617505763564278546 = property(__get_f_2617505763564278546,
                                     __set_f_2617505763564278546)
    f_6226735239301116980 = property(__get_f_6226735239301116980,
                                     __set_f_6226735239301116980)
    f_668843506724768408 = property(__get_f_668843506724768408,
                                    __set_f_668843506724768408)
    f_6402563436718652275 = property(__get_f_6402563436718652275,
                                     __set_f_6402563436718652275)
    f_7097397218627294709 = property(__get_f_7097397218627294709,
                                     __set_f_7097397218627294709)
    f_4207545581028892358 = property(__get_f_4207545581028892358,
                                     __set_f_4207545581028892358)
    f_4739546102366045703 = property(__get_f_4739546102366045703,
                                     __set_f_4739546102366045703)
    f_2824798772165075035 = property(__get_f_2824798772165075035,
                                     __set_f_2824798772165075035)
    f_2112052519892767027 = property(__get_f_2112052519892767027,
                                     __set_f_2112052519892767027)


class inst_i_6471126574510039166(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_8011412086637413419: [CCRCLR, 8]  # type: ignore
    __f_8525072872364582718: [int, 4]  # type: ignore
    __f_5764488542934669646: [ADDR_GLB_8_WITHOUT_BANK, 21]  # type: ignore
    __f_3111809177143691821: [datatype.uint16, 16]  # type: ignore
    __f_8910660727579538404: [datatype.uint16, 16]  # type: ignore
    __f_1090056923820809010: [datatype.uint16, 16]  # type: ignore
    __f_2792798599134201914: [datatype.uint16, 16]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, int, ADDR_GLB_8_WITHOUT_BANK, int, int,
                               int, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(7)

        self.__f_2792798599134201914 = int(0)
        cf_str += '>u16'
        self.__f_1090056923820809010 = int(0)
        cf_str += '>u16'
        self.__f_8910660727579538404 = int(0)
        cf_str += '>u16'
        self.__f_3111809177143691821 = int(0)
        cf_str += '>u16'
        self.__f_5764488542934669646 = ADDR_GLB_8_WITHOUT_BANK(0)
        cf_str += '>u21'
        self.__f_8525072872364582718 = int(0)
        cf_str += '>u4'
        self.__f_8011412086637413419 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(67)

    def fields(
        self,
        f_8011412086637413419: CCRCLR = None,
        f_8525072872364582718: int = None,
        f_5764488542934669646: ADDR_GLB_8_WITHOUT_BANK = None,
        f_3111809177143691821: int = None,
        f_8910660727579538404: int = None,
        f_1090056923820809010: int = None,
        f_2792798599134201914: int = None,
    ):
        if f_8011412086637413419:
            self.f_8011412086637413419 = f_8011412086637413419
        if f_8525072872364582718:
            self.f_8525072872364582718 = f_8525072872364582718
        if f_5764488542934669646:
            self.f_5764488542934669646 = f_5764488542934669646
        if f_3111809177143691821:
            self.f_3111809177143691821 = f_3111809177143691821
        if f_8910660727579538404:
            self.f_8910660727579538404 = f_8910660727579538404
        if f_1090056923820809010:
            self.f_1090056923820809010 = f_1090056923820809010
        if f_2792798599134201914:
            self.f_2792798599134201914 = f_2792798599134201914
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_2792798599134201914),
            int(self.f_1090056923820809010),
            int(self.f_8910660727579538404),
            int(self.f_3111809177143691821),
            int(self.f_5764488542934669646),
            int(self.f_8525072872364582718),
            int(self.f_8011412086637413419),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 14
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x43
        (
            self.f_2792798599134201914,
            self.f_1090056923820809010,
            self.f_8910660727579538404,
            self.f_3111809177143691821,
            self.f_5764488542934669646,
            self.f_8525072872364582718,
            self.f_8011412086637413419,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_6471126574510039166(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_6471126574510039166().fields(\n'
        res += '\tf_8011412086637413419 = %s ,\n' % str(
            self.f_8011412086637413419)
        res += '\tf_8525072872364582718 = %s ,\n' % str(
            self.f_8525072872364582718)
        res += '\tf_5764488542934669646 = %s ,\n' % str(
            self.f_5764488542934669646)
        res += '\tf_3111809177143691821 = %s ,\n' % str(
            self.f_3111809177143691821)
        res += '\tf_8910660727579538404 = %s ,\n' % str(
            self.f_8910660727579538404)
        res += '\tf_1090056923820809010 = %s ,\n' % str(
            self.f_1090056923820809010)
        res += '\tf_2792798599134201914 = %s ,\n' % str(
            self.f_2792798599134201914)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 14

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_8011412086637413419(self):
        return self.__f_8011412086637413419

    def __set_f_8011412086637413419(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_8011412086637413419 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_8525072872364582718(self):
        return self.__f_8525072872364582718

    def __set_f_8525072872364582718(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_8525072872364582718 = int(value)

    def __get_f_5764488542934669646(self):
        return self.__f_5764488542934669646

    def __set_f_5764488542934669646(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITHOUT_BANK)))
        self.__f_5764488542934669646 = value if isinstance(
            value, ADDR_GLB_8_WITHOUT_BANK) else ADDR_GLB_8_WITHOUT_BANK(value)

    def __get_f_3111809177143691821(self):
        return self.__f_3111809177143691821

    def __set_f_3111809177143691821(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_3111809177143691821 = int(value)

    def __get_f_8910660727579538404(self):
        return self.__f_8910660727579538404

    def __set_f_8910660727579538404(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8910660727579538404 = int(value)

    def __get_f_1090056923820809010(self):
        return self.__f_1090056923820809010

    def __set_f_1090056923820809010(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1090056923820809010 = int(value)

    def __get_f_2792798599134201914(self):
        return self.__f_2792798599134201914

    def __set_f_2792798599134201914(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_2792798599134201914 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_8011412086637413419 = property(__get_f_8011412086637413419,
                                     __set_f_8011412086637413419)
    f_8525072872364582718 = property(__get_f_8525072872364582718,
                                     __set_f_8525072872364582718)
    f_5764488542934669646 = property(__get_f_5764488542934669646,
                                     __set_f_5764488542934669646)
    f_3111809177143691821 = property(__get_f_3111809177143691821,
                                     __set_f_3111809177143691821)
    f_8910660727579538404 = property(__get_f_8910660727579538404,
                                     __set_f_8910660727579538404)
    f_1090056923820809010 = property(__get_f_1090056923820809010,
                                     __set_f_1090056923820809010)
    f_2792798599134201914 = property(__get_f_2792798599134201914,
                                     __set_f_2792798599134201914)


class inst_i_6369672458787877517(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_8525072872364582718: [int, 4]  # type: ignore
    __f_2112052519892767027: [int, 4]  # type: ignore
    __f_5031038292015147394: [int, 1]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int, int, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(7)

        self.__f_5031038292015147394 = int(0)
        cf_str += '>u1'
        self.__f_2112052519892767027 = int(0)
        cf_str += '>u4'
        self.__f_8525072872364582718 = int(0)
        cf_str += '>u4'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(68)

    def fields(
        self,
        f_8525072872364582718: int = None,
        f_2112052519892767027: int = None,
        f_5031038292015147394: int = None,
    ):
        if f_8525072872364582718:
            self.f_8525072872364582718 = f_8525072872364582718
        if f_2112052519892767027:
            self.f_2112052519892767027 = f_2112052519892767027
        if f_5031038292015147394:
            self.f_5031038292015147394 = f_5031038292015147394
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_5031038292015147394),
            int(self.f_2112052519892767027),
            int(self.f_8525072872364582718),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 3
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x44
        (
            self.f_5031038292015147394,
            self.f_2112052519892767027,
            self.f_8525072872364582718,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_6369672458787877517(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_6369672458787877517().fields(\n'
        res += '\tf_8525072872364582718 = %s ,\n' % str(
            self.f_8525072872364582718)
        res += '\tf_2112052519892767027 = %s ,\n' % str(
            self.f_2112052519892767027)
        res += '\tf_5031038292015147394 = %s ,\n' % str(
            self.f_5031038292015147394)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 3

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_8525072872364582718(self):
        return self.__f_8525072872364582718

    def __set_f_8525072872364582718(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_8525072872364582718 = int(value)

    def __get_f_2112052519892767027(self):
        return self.__f_2112052519892767027

    def __set_f_2112052519892767027(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_2112052519892767027 = int(value)

    def __get_f_5031038292015147394(self):
        return self.__f_5031038292015147394

    def __set_f_5031038292015147394(self, value):
        assert int(value) < 2**1

        assert int(value) >= 0

        self.__f_5031038292015147394 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_8525072872364582718 = property(__get_f_8525072872364582718,
                                     __set_f_8525072872364582718)
    f_2112052519892767027 = property(__get_f_2112052519892767027,
                                     __set_f_2112052519892767027)
    f_5031038292015147394 = property(__get_f_5031038292015147394,
                                     __set_f_5031038292015147394)


class inst_i_7025294518658670577(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_2921210218837521005: [CCRCLR, 8]  # type: ignore
    __f_8525072872364582718: [int, 4]  # type: ignore
    __f_4535149732094779661: [ADDR_GLB_8_WITHOUT_BANK, 21]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, int, ADDR_GLB_8_WITHOUT_BANK,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(7)

        self.__f_4535149732094779661 = ADDR_GLB_8_WITHOUT_BANK(0)
        cf_str += '>u21'
        self.__f_8525072872364582718 = int(0)
        cf_str += '>u4'
        self.__f_2921210218837521005 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(69)

    def fields(
        self,
        f_2921210218837521005: CCRCLR = None,
        f_8525072872364582718: int = None,
        f_4535149732094779661: ADDR_GLB_8_WITHOUT_BANK = None,
    ):
        if f_2921210218837521005:
            self.f_2921210218837521005 = f_2921210218837521005
        if f_8525072872364582718:
            self.f_8525072872364582718 = f_8525072872364582718
        if f_4535149732094779661:
            self.f_4535149732094779661 = f_4535149732094779661
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_4535149732094779661),
            int(self.f_8525072872364582718),
            int(self.f_2921210218837521005),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 6
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x45
        (
            self.f_4535149732094779661,
            self.f_8525072872364582718,
            self.f_2921210218837521005,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_7025294518658670577(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_7025294518658670577().fields(\n'
        res += '\tf_2921210218837521005 = %s ,\n' % str(
            self.f_2921210218837521005)
        res += '\tf_8525072872364582718 = %s ,\n' % str(
            self.f_8525072872364582718)
        res += '\tf_4535149732094779661 = %s ,\n' % str(
            self.f_4535149732094779661)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 6

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_2921210218837521005(self):
        return self.__f_2921210218837521005

    def __set_f_2921210218837521005(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_2921210218837521005 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_8525072872364582718(self):
        return self.__f_8525072872364582718

    def __set_f_8525072872364582718(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_8525072872364582718 = int(value)

    def __get_f_4535149732094779661(self):
        return self.__f_4535149732094779661

    def __set_f_4535149732094779661(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITHOUT_BANK)))
        self.__f_4535149732094779661 = value if isinstance(
            value, ADDR_GLB_8_WITHOUT_BANK) else ADDR_GLB_8_WITHOUT_BANK(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_2921210218837521005 = property(__get_f_2921210218837521005,
                                     __set_f_2921210218837521005)
    f_8525072872364582718 = property(__get_f_8525072872364582718,
                                     __set_f_8525072872364582718)
    f_4535149732094779661 = property(__get_f_4535149732094779661,
                                     __set_f_4535149732094779661)


class inst_i_6731377247628139860(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_8525072872364582718: [int, 4]  # type: ignore
    __f_7551535371612946385: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_581203445514181141: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_729035510703121801: [datatype.uint16, 16]  # type: ignore
    __f_6668041380037753856: [datatype.uint16, 16]  # type: ignore
    __f_1840283918827822297: [datatype.uint16, 16]  # type: ignore
    __f_910628193515839991: [datatype.uint16, 16]  # type: ignore
    __f_6174243932487844318: [STRIDE_GLB, 64]  # type: ignore
    __f_4778958858443013090: [STRIDE_GLB, 64]  # type: ignore
    __f_1365507571385172390: [int, 4]  # type: ignore
    __f_215085022235903655: [PRECISION, 2]  # type: ignore
    __f_1770559390771253019: [QUAN_SIGNED, 1]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int, ADDR_GLB_8_WITH_BANK, ADDR_GLB_8_WITH_BANK,
                               int, int, int, int, STRIDE_GLB, STRIDE_GLB, int,
                               PRECISION, QUAN_SIGNED,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(3)

        self.__f_1770559390771253019 = QUAN_SIGNED(0)
        cf_str += '>u1'
        self.__f_215085022235903655 = PRECISION(0)
        cf_str += '>u2'
        self.__f_1365507571385172390 = int(0)
        cf_str += '>u4'
        self.__f_4778958858443013090 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_6174243932487844318 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_910628193515839991 = int(0)
        cf_str += '>u16'
        self.__f_1840283918827822297 = int(0)
        cf_str += '>u16'
        self.__f_6668041380037753856 = int(0)
        cf_str += '>u16'
        self.__f_729035510703121801 = int(0)
        cf_str += '>u16'
        self.__f_581203445514181141 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_7551535371612946385 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_8525072872364582718 = int(0)
        cf_str += '>u4'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(70)

    def fields(
        self,
        f_8525072872364582718: int = None,
        f_7551535371612946385: ADDR_GLB_8_WITH_BANK = None,
        f_581203445514181141: ADDR_GLB_8_WITH_BANK = None,
        f_729035510703121801: int = None,
        f_6668041380037753856: int = None,
        f_1840283918827822297: int = None,
        f_910628193515839991: int = None,
        f_6174243932487844318: STRIDE_GLB = None,
        f_4778958858443013090: STRIDE_GLB = None,
        f_1365507571385172390: int = None,
        f_215085022235903655: PRECISION = None,
        f_1770559390771253019: QUAN_SIGNED = None,
    ):
        if f_8525072872364582718:
            self.f_8525072872364582718 = f_8525072872364582718
        if f_7551535371612946385:
            self.f_7551535371612946385 = f_7551535371612946385
        if f_581203445514181141:
            self.f_581203445514181141 = f_581203445514181141
        if f_729035510703121801:
            self.f_729035510703121801 = f_729035510703121801
        if f_6668041380037753856:
            self.f_6668041380037753856 = f_6668041380037753856
        if f_1840283918827822297:
            self.f_1840283918827822297 = f_1840283918827822297
        if f_910628193515839991:
            self.f_910628193515839991 = f_910628193515839991
        if f_6174243932487844318:
            self.f_6174243932487844318 = f_6174243932487844318
        if f_4778958858443013090:
            self.f_4778958858443013090 = f_4778958858443013090
        if f_1365507571385172390:
            self.f_1365507571385172390 = f_1365507571385172390
        if f_215085022235903655:
            self.f_215085022235903655 = f_215085022235903655
        if f_1770559390771253019:
            self.f_1770559390771253019 = f_1770559390771253019
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_1770559390771253019),
            int(self.f_215085022235903655),
            int(self.f_1365507571385172390),
            int(self.f_4778958858443013090),
            int(self.f_6174243932487844318),
            int(self.f_910628193515839991),
            int(self.f_1840283918827822297),
            int(self.f_6668041380037753856),
            int(self.f_729035510703121801),
            int(self.f_581203445514181141),
            int(self.f_7551535371612946385),
            int(self.f_8525072872364582718),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 33
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x46
        (
            self.f_1770559390771253019,
            self.f_215085022235903655,
            self.f_1365507571385172390,
            self.f_4778958858443013090,
            self.f_6174243932487844318,
            self.f_910628193515839991,
            self.f_1840283918827822297,
            self.f_6668041380037753856,
            self.f_729035510703121801,
            self.f_581203445514181141,
            self.f_7551535371612946385,
            self.f_8525072872364582718,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_6731377247628139860(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_6731377247628139860().fields(\n'
        res += '\tf_8525072872364582718 = %s ,\n' % str(
            self.f_8525072872364582718)
        res += '\tf_7551535371612946385 = %s ,\n' % str(
            self.f_7551535371612946385)
        res += '\tf_581203445514181141 = %s ,\n' % str(
            self.f_581203445514181141)
        res += '\tf_729035510703121801 = %s ,\n' % str(
            self.f_729035510703121801)
        res += '\tf_6668041380037753856 = %s ,\n' % str(
            self.f_6668041380037753856)
        res += '\tf_1840283918827822297 = %s ,\n' % str(
            self.f_1840283918827822297)
        res += '\tf_910628193515839991 = %s ,\n' % str(
            self.f_910628193515839991)
        res += '\tf_6174243932487844318 = %s ,\n' % str(
            self.f_6174243932487844318)
        res += '\tf_4778958858443013090 = %s ,\n' % str(
            self.f_4778958858443013090)
        res += '\tf_1365507571385172390 = %s ,\n' % str(
            self.f_1365507571385172390)
        res += '\tf_215085022235903655 = %s ,\n' % str(
            self.f_215085022235903655)
        res += '\tf_1770559390771253019 = %s ,\n' % str(
            self.f_1770559390771253019)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 33

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_8525072872364582718(self):
        return self.__f_8525072872364582718

    def __set_f_8525072872364582718(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_8525072872364582718 = int(value)

    def __get_f_7551535371612946385(self):
        return self.__f_7551535371612946385

    def __set_f_7551535371612946385(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_7551535371612946385 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_581203445514181141(self):
        return self.__f_581203445514181141

    def __set_f_581203445514181141(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_581203445514181141 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_729035510703121801(self):
        return self.__f_729035510703121801

    def __set_f_729035510703121801(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_729035510703121801 = int(value)

    def __get_f_6668041380037753856(self):
        return self.__f_6668041380037753856

    def __set_f_6668041380037753856(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_6668041380037753856 = int(value)

    def __get_f_1840283918827822297(self):
        return self.__f_1840283918827822297

    def __set_f_1840283918827822297(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1840283918827822297 = int(value)

    def __get_f_910628193515839991(self):
        return self.__f_910628193515839991

    def __set_f_910628193515839991(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_910628193515839991 = int(value)

    def __get_f_6174243932487844318(self):
        return self.__f_6174243932487844318

    def __set_f_6174243932487844318(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_6174243932487844318 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_4778958858443013090(self):
        return self.__f_4778958858443013090

    def __set_f_4778958858443013090(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_4778958858443013090 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_1365507571385172390(self):
        return self.__f_1365507571385172390

    def __set_f_1365507571385172390(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_1365507571385172390 = int(value)

    def __get_f_215085022235903655(self):
        return self.__f_215085022235903655

    def __set_f_215085022235903655(self, value):

        assert (isinstance(value, (int, PRECISION)))
        self.__f_215085022235903655 = value if isinstance(
            value, PRECISION) else PRECISION(value)

    def __get_f_1770559390771253019(self):
        return self.__f_1770559390771253019

    def __set_f_1770559390771253019(self, value):

        assert (isinstance(value, (int, QUAN_SIGNED)))
        self.__f_1770559390771253019 = value if isinstance(
            value, QUAN_SIGNED) else QUAN_SIGNED(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_8525072872364582718 = property(__get_f_8525072872364582718,
                                     __set_f_8525072872364582718)
    f_7551535371612946385 = property(__get_f_7551535371612946385,
                                     __set_f_7551535371612946385)
    f_581203445514181141 = property(__get_f_581203445514181141,
                                    __set_f_581203445514181141)
    f_729035510703121801 = property(__get_f_729035510703121801,
                                    __set_f_729035510703121801)
    f_6668041380037753856 = property(__get_f_6668041380037753856,
                                     __set_f_6668041380037753856)
    f_1840283918827822297 = property(__get_f_1840283918827822297,
                                     __set_f_1840283918827822297)
    f_910628193515839991 = property(__get_f_910628193515839991,
                                    __set_f_910628193515839991)
    f_6174243932487844318 = property(__get_f_6174243932487844318,
                                     __set_f_6174243932487844318)
    f_4778958858443013090 = property(__get_f_4778958858443013090,
                                     __set_f_4778958858443013090)
    f_1365507571385172390 = property(__get_f_1365507571385172390,
                                     __set_f_1365507571385172390)
    f_215085022235903655 = property(__get_f_215085022235903655,
                                    __set_f_215085022235903655)
    f_1770559390771253019 = property(__get_f_1770559390771253019,
                                     __set_f_1770559390771253019)


class inst_i_5088819369833811485(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_8525072872364582718: [int, 4]  # type: ignore
    __f_9004242308200849329: [int, 5]  # type: ignore
    __f_7028639040274240580: [int, 5]  # type: ignore
    __f_3175614108873140434: [int, 5]  # type: ignore
    __f_592763409212270165: [int, 5]  # type: ignore
    __f_4345176537083219404: [datatype.uint8, 8]  # type: ignore
    __f_4437090942066219399: [datatype.uint8, 8]  # type: ignore
    __f_2367561162708418741: [int, 5]  # type: ignore
    __f_2921827088950148559: [datatype.uint16, 16]  # type: ignore
    __f_6719836634322234378: [datatype.uint16, 16]  # type: ignore
    __f_3217332499044511084: [TCU_MODE, 2]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int, int, int, int, int, int, int, int, int, int,
                               TCU_MODE,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(1)

        self.__f_3217332499044511084 = TCU_MODE(0)
        cf_str += '>u2'
        self.__f_6719836634322234378 = int(0)
        cf_str += '>u16'
        self.__f_2921827088950148559 = int(0)
        cf_str += '>u16'
        self.__f_2367561162708418741 = int(0)
        cf_str += '>u5'
        self.__f_4437090942066219399 = int(0)
        cf_str += '>u8'
        self.__f_4345176537083219404 = int(0)
        cf_str += '>u8'
        self.__f_592763409212270165 = int(0)
        cf_str += '>u5'
        self.__f_3175614108873140434 = int(0)
        cf_str += '>u5'
        self.__f_7028639040274240580 = int(0)
        cf_str += '>u5'
        self.__f_9004242308200849329 = int(0)
        cf_str += '>u5'
        self.__f_8525072872364582718 = int(0)
        cf_str += '>u4'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(71)

    def fields(
        self,
        f_8525072872364582718: int = None,
        f_9004242308200849329: int = None,
        f_7028639040274240580: int = None,
        f_3175614108873140434: int = None,
        f_592763409212270165: int = None,
        f_4345176537083219404: int = None,
        f_4437090942066219399: int = None,
        f_2367561162708418741: int = None,
        f_2921827088950148559: int = None,
        f_6719836634322234378: int = None,
        f_3217332499044511084: TCU_MODE = None,
    ):
        if f_8525072872364582718:
            self.f_8525072872364582718 = f_8525072872364582718
        if f_9004242308200849329:
            self.f_9004242308200849329 = f_9004242308200849329
        if f_7028639040274240580:
            self.f_7028639040274240580 = f_7028639040274240580
        if f_3175614108873140434:
            self.f_3175614108873140434 = f_3175614108873140434
        if f_592763409212270165:
            self.f_592763409212270165 = f_592763409212270165
        if f_4345176537083219404:
            self.f_4345176537083219404 = f_4345176537083219404
        if f_4437090942066219399:
            self.f_4437090942066219399 = f_4437090942066219399
        if f_2367561162708418741:
            self.f_2367561162708418741 = f_2367561162708418741
        if f_2921827088950148559:
            self.f_2921827088950148559 = f_2921827088950148559
        if f_6719836634322234378:
            self.f_6719836634322234378 = f_6719836634322234378
        if f_3217332499044511084:
            self.f_3217332499044511084 = f_3217332499044511084
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_3217332499044511084),
            int(self.f_6719836634322234378),
            int(self.f_2921827088950148559),
            int(self.f_2367561162708418741),
            int(self.f_4437090942066219399),
            int(self.f_4345176537083219404),
            int(self.f_592763409212270165),
            int(self.f_3175614108873140434),
            int(self.f_7028639040274240580),
            int(self.f_9004242308200849329),
            int(self.f_8525072872364582718),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 11
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x47
        (
            self.f_3217332499044511084,
            self.f_6719836634322234378,
            self.f_2921827088950148559,
            self.f_2367561162708418741,
            self.f_4437090942066219399,
            self.f_4345176537083219404,
            self.f_592763409212270165,
            self.f_3175614108873140434,
            self.f_7028639040274240580,
            self.f_9004242308200849329,
            self.f_8525072872364582718,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_5088819369833811485(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_5088819369833811485().fields(\n'
        res += '\tf_8525072872364582718 = %s ,\n' % str(
            self.f_8525072872364582718)
        res += '\tf_9004242308200849329 = %s ,\n' % str(
            self.f_9004242308200849329)
        res += '\tf_7028639040274240580 = %s ,\n' % str(
            self.f_7028639040274240580)
        res += '\tf_3175614108873140434 = %s ,\n' % str(
            self.f_3175614108873140434)
        res += '\tf_592763409212270165 = %s ,\n' % str(
            self.f_592763409212270165)
        res += '\tf_4345176537083219404 = %s ,\n' % str(
            self.f_4345176537083219404)
        res += '\tf_4437090942066219399 = %s ,\n' % str(
            self.f_4437090942066219399)
        res += '\tf_2367561162708418741 = %s ,\n' % str(
            self.f_2367561162708418741)
        res += '\tf_2921827088950148559 = %s ,\n' % str(
            self.f_2921827088950148559)
        res += '\tf_6719836634322234378 = %s ,\n' % str(
            self.f_6719836634322234378)
        res += '\tf_3217332499044511084 = %s ,\n' % str(
            self.f_3217332499044511084)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 11

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_8525072872364582718(self):
        return self.__f_8525072872364582718

    def __set_f_8525072872364582718(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_8525072872364582718 = int(value)

    def __get_f_9004242308200849329(self):
        return self.__f_9004242308200849329

    def __set_f_9004242308200849329(self, value):
        assert int(value) < 2**5

        assert int(value) >= 0

        self.__f_9004242308200849329 = int(value)

    def __get_f_7028639040274240580(self):
        return self.__f_7028639040274240580

    def __set_f_7028639040274240580(self, value):
        assert int(value) < 2**5

        assert int(value) >= 0

        self.__f_7028639040274240580 = int(value)

    def __get_f_3175614108873140434(self):
        return self.__f_3175614108873140434

    def __set_f_3175614108873140434(self, value):
        assert int(value) < 2**5

        assert int(value) >= 0

        self.__f_3175614108873140434 = int(value)

    def __get_f_592763409212270165(self):
        return self.__f_592763409212270165

    def __set_f_592763409212270165(self, value):
        assert int(value) < 2**5

        assert int(value) >= 0

        self.__f_592763409212270165 = int(value)

    def __get_f_4345176537083219404(self):
        return self.__f_4345176537083219404

    def __set_f_4345176537083219404(self, value):
        assert int(value) < 2**8

        assert int(value) >= 0

        self.__f_4345176537083219404 = int(value)

    def __get_f_4437090942066219399(self):
        return self.__f_4437090942066219399

    def __set_f_4437090942066219399(self, value):
        assert int(value) < 2**8

        assert int(value) >= 0

        self.__f_4437090942066219399 = int(value)

    def __get_f_2367561162708418741(self):
        return self.__f_2367561162708418741

    def __set_f_2367561162708418741(self, value):
        assert int(value) < 2**5

        assert int(value) >= 0

        self.__f_2367561162708418741 = int(value)

    def __get_f_2921827088950148559(self):
        return self.__f_2921827088950148559

    def __set_f_2921827088950148559(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_2921827088950148559 = int(value)

    def __get_f_6719836634322234378(self):
        return self.__f_6719836634322234378

    def __set_f_6719836634322234378(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_6719836634322234378 = int(value)

    def __get_f_3217332499044511084(self):
        return self.__f_3217332499044511084

    def __set_f_3217332499044511084(self, value):

        assert (isinstance(value, (int, TCU_MODE)))
        self.__f_3217332499044511084 = value if isinstance(
            value, TCU_MODE) else TCU_MODE(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_8525072872364582718 = property(__get_f_8525072872364582718,
                                     __set_f_8525072872364582718)
    f_9004242308200849329 = property(__get_f_9004242308200849329,
                                     __set_f_9004242308200849329)
    f_7028639040274240580 = property(__get_f_7028639040274240580,
                                     __set_f_7028639040274240580)
    f_3175614108873140434 = property(__get_f_3175614108873140434,
                                     __set_f_3175614108873140434)
    f_592763409212270165 = property(__get_f_592763409212270165,
                                    __set_f_592763409212270165)
    f_4345176537083219404 = property(__get_f_4345176537083219404,
                                     __set_f_4345176537083219404)
    f_4437090942066219399 = property(__get_f_4437090942066219399,
                                     __set_f_4437090942066219399)
    f_2367561162708418741 = property(__get_f_2367561162708418741,
                                     __set_f_2367561162708418741)
    f_2921827088950148559 = property(__get_f_2921827088950148559,
                                     __set_f_2921827088950148559)
    f_6719836634322234378 = property(__get_f_6719836634322234378,
                                     __set_f_6719836634322234378)
    f_3217332499044511084 = property(__get_f_3217332499044511084,
                                     __set_f_3217332499044511084)


class inst_i_7758253786169375348(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_8525072872364582718: [int, 4]  # type: ignore
    __f_4858117442824963759: [datatype.uint16, 16]  # type: ignore
    __f_8686416599711569530: [datatype.uint16, 16]  # type: ignore
    __f_3293752958096851720: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int, int, int, ADDR_GLB_8_WITH_BANK,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(3)

        self.__f_3293752958096851720 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_8686416599711569530 = int(0)
        cf_str += '>u16'
        self.__f_4858117442824963759 = int(0)
        cf_str += '>u16'
        self.__f_8525072872364582718 = int(0)
        cf_str += '>u4'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(72)

    def fields(
        self,
        f_8525072872364582718: int = None,
        f_4858117442824963759: int = None,
        f_8686416599711569530: int = None,
        f_3293752958096851720: ADDR_GLB_8_WITH_BANK = None,
    ):
        if f_8525072872364582718:
            self.f_8525072872364582718 = f_8525072872364582718
        if f_4858117442824963759:
            self.f_4858117442824963759 = f_4858117442824963759
        if f_8686416599711569530:
            self.f_8686416599711569530 = f_8686416599711569530
        if f_3293752958096851720:
            self.f_3293752958096851720 = f_3293752958096851720
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_3293752958096851720),
            int(self.f_8686416599711569530),
            int(self.f_4858117442824963759),
            int(self.f_8525072872364582718),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 9
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x48
        (
            self.f_3293752958096851720,
            self.f_8686416599711569530,
            self.f_4858117442824963759,
            self.f_8525072872364582718,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_7758253786169375348(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_7758253786169375348().fields(\n'
        res += '\tf_8525072872364582718 = %s ,\n' % str(
            self.f_8525072872364582718)
        res += '\tf_4858117442824963759 = %s ,\n' % str(
            self.f_4858117442824963759)
        res += '\tf_8686416599711569530 = %s ,\n' % str(
            self.f_8686416599711569530)
        res += '\tf_3293752958096851720 = %s ,\n' % str(
            self.f_3293752958096851720)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 9

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_8525072872364582718(self):
        return self.__f_8525072872364582718

    def __set_f_8525072872364582718(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_8525072872364582718 = int(value)

    def __get_f_4858117442824963759(self):
        return self.__f_4858117442824963759

    def __set_f_4858117442824963759(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_4858117442824963759 = int(value)

    def __get_f_8686416599711569530(self):
        return self.__f_8686416599711569530

    def __set_f_8686416599711569530(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8686416599711569530 = int(value)

    def __get_f_3293752958096851720(self):
        return self.__f_3293752958096851720

    def __set_f_3293752958096851720(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_3293752958096851720 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_8525072872364582718 = property(__get_f_8525072872364582718,
                                     __set_f_8525072872364582718)
    f_4858117442824963759 = property(__get_f_4858117442824963759,
                                     __set_f_4858117442824963759)
    f_8686416599711569530 = property(__get_f_8686416599711569530,
                                     __set_f_8686416599711569530)
    f_3293752958096851720 = property(__get_f_3293752958096851720,
                                     __set_f_3293752958096851720)


class inst_i_8336797519624639034(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_8175951596209014998: [CCRCLR, 8]  # type: ignore
    __f_2871215043598640192: [CCRCLR, 8]  # type: ignore
    __f_1851582658599760477: [CCRSET, 11]  # type: ignore
    __f_8525072872364582718: [int, 4]  # type: ignore
    __f_2988226083445662793: [int, 1]  # type: ignore
    __f_4547371210035592152: [int, 1]  # type: ignore
    __f_7892763318645684031: [int, 1]  # type: ignore
    __f_9158500683338375818: [int, 4]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, CCRCLR, CCRSET, int, int, int, int,
                               int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(2)

        self.__f_9158500683338375818 = int(0)
        cf_str += '>u4'
        self.__f_7892763318645684031 = int(0)
        cf_str += '>u1'
        self.__f_4547371210035592152 = int(0)
        cf_str += '>u1'
        self.__f_2988226083445662793 = int(0)
        cf_str += '>u1'
        self.__f_8525072872364582718 = int(0)
        cf_str += '>u4'
        self.__f_1851582658599760477 = CCRSET(0)
        cf_str += '>u11'
        self.__f_2871215043598640192 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_8175951596209014998 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(73)

    def fields(
        self,
        f_8175951596209014998: CCRCLR = None,
        f_2871215043598640192: CCRCLR = None,
        f_1851582658599760477: CCRSET = None,
        f_8525072872364582718: int = None,
        f_2988226083445662793: int = None,
        f_4547371210035592152: int = None,
        f_7892763318645684031: int = None,
        f_9158500683338375818: int = None,
    ):
        if f_8175951596209014998:
            self.f_8175951596209014998 = f_8175951596209014998
        if f_2871215043598640192:
            self.f_2871215043598640192 = f_2871215043598640192
        if f_1851582658599760477:
            self.f_1851582658599760477 = f_1851582658599760477
        if f_8525072872364582718:
            self.f_8525072872364582718 = f_8525072872364582718
        if f_2988226083445662793:
            self.f_2988226083445662793 = f_2988226083445662793
        if f_4547371210035592152:
            self.f_4547371210035592152 = f_4547371210035592152
        if f_7892763318645684031:
            self.f_7892763318645684031 = f_7892763318645684031
        if f_9158500683338375818:
            self.f_9158500683338375818 = f_9158500683338375818
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_9158500683338375818),
            int(self.f_7892763318645684031),
            int(self.f_4547371210035592152),
            int(self.f_2988226083445662793),
            int(self.f_8525072872364582718),
            int(self.f_1851582658599760477),
            int(self.f_2871215043598640192),
            int(self.f_8175951596209014998),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 6
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x49
        (
            self.f_9158500683338375818,
            self.f_7892763318645684031,
            self.f_4547371210035592152,
            self.f_2988226083445662793,
            self.f_8525072872364582718,
            self.f_1851582658599760477,
            self.f_2871215043598640192,
            self.f_8175951596209014998,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_8336797519624639034(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_8336797519624639034().fields(\n'
        res += '\tf_8175951596209014998 = %s ,\n' % str(
            self.f_8175951596209014998)
        res += '\tf_2871215043598640192 = %s ,\n' % str(
            self.f_2871215043598640192)
        res += '\tf_1851582658599760477 = %s ,\n' % str(
            self.f_1851582658599760477)
        res += '\tf_8525072872364582718 = %s ,\n' % str(
            self.f_8525072872364582718)
        res += '\tf_2988226083445662793 = %s ,\n' % str(
            self.f_2988226083445662793)
        res += '\tf_4547371210035592152 = %s ,\n' % str(
            self.f_4547371210035592152)
        res += '\tf_7892763318645684031 = %s ,\n' % str(
            self.f_7892763318645684031)
        res += '\tf_9158500683338375818 = %s ,\n' % str(
            self.f_9158500683338375818)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 6

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_8175951596209014998(self):
        return self.__f_8175951596209014998

    def __set_f_8175951596209014998(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_8175951596209014998 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_2871215043598640192(self):
        return self.__f_2871215043598640192

    def __set_f_2871215043598640192(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_2871215043598640192 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1851582658599760477(self):
        return self.__f_1851582658599760477

    def __set_f_1851582658599760477(self, value):

        assert (isinstance(value, (int, CCRSET)))
        self.__f_1851582658599760477 = value if isinstance(
            value, CCRSET) else CCRSET(value)

    def __get_f_8525072872364582718(self):
        return self.__f_8525072872364582718

    def __set_f_8525072872364582718(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_8525072872364582718 = int(value)

    def __get_f_2988226083445662793(self):
        return self.__f_2988226083445662793

    def __set_f_2988226083445662793(self, value):
        assert int(value) < 2**1

        assert int(value) >= 0

        self.__f_2988226083445662793 = int(value)

    def __get_f_4547371210035592152(self):
        return self.__f_4547371210035592152

    def __set_f_4547371210035592152(self, value):
        assert int(value) < 2**1

        assert int(value) >= 0

        self.__f_4547371210035592152 = int(value)

    def __get_f_7892763318645684031(self):
        return self.__f_7892763318645684031

    def __set_f_7892763318645684031(self, value):
        assert int(value) < 2**1

        assert int(value) >= 0

        self.__f_7892763318645684031 = int(value)

    def __get_f_9158500683338375818(self):
        return self.__f_9158500683338375818

    def __set_f_9158500683338375818(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_9158500683338375818 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_8175951596209014998 = property(__get_f_8175951596209014998,
                                     __set_f_8175951596209014998)
    f_2871215043598640192 = property(__get_f_2871215043598640192,
                                     __set_f_2871215043598640192)
    f_1851582658599760477 = property(__get_f_1851582658599760477,
                                     __set_f_1851582658599760477)
    f_8525072872364582718 = property(__get_f_8525072872364582718,
                                     __set_f_8525072872364582718)
    f_2988226083445662793 = property(__get_f_2988226083445662793,
                                     __set_f_2988226083445662793)
    f_4547371210035592152 = property(__get_f_4547371210035592152,
                                     __set_f_4547371210035592152)
    f_7892763318645684031 = property(__get_f_7892763318645684031,
                                     __set_f_7892763318645684031)
    f_9158500683338375818 = property(__get_f_9158500683338375818,
                                     __set_f_9158500683338375818)


class inst_i_2090902360472978351(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_8525072872364582718: [int, 4]  # type: ignore
    __f_8311800582383395327: [STRIDE_GLB, 64]  # type: ignore
    __f_4875701691136722882: [STRIDE_GLB, 64]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int, STRIDE_GLB, STRIDE_GLB,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(4)

        self.__f_4875701691136722882 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_8311800582383395327 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_8525072872364582718 = int(0)
        cf_str += '>u4'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(74)

    def fields(
        self,
        f_8525072872364582718: int = None,
        f_8311800582383395327: STRIDE_GLB = None,
        f_4875701691136722882: STRIDE_GLB = None,
    ):
        if f_8525072872364582718:
            self.f_8525072872364582718 = f_8525072872364582718
        if f_8311800582383395327:
            self.f_8311800582383395327 = f_8311800582383395327
        if f_4875701691136722882:
            self.f_4875701691136722882 = f_4875701691136722882
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_4875701691136722882),
            int(self.f_8311800582383395327),
            int(self.f_8525072872364582718),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 18
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x4a
        (
            self.f_4875701691136722882,
            self.f_8311800582383395327,
            self.f_8525072872364582718,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_2090902360472978351(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_2090902360472978351().fields(\n'
        res += '\tf_8525072872364582718 = %s ,\n' % str(
            self.f_8525072872364582718)
        res += '\tf_8311800582383395327 = %s ,\n' % str(
            self.f_8311800582383395327)
        res += '\tf_4875701691136722882 = %s ,\n' % str(
            self.f_4875701691136722882)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 18

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_8525072872364582718(self):
        return self.__f_8525072872364582718

    def __set_f_8525072872364582718(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_8525072872364582718 = int(value)

    def __get_f_8311800582383395327(self):
        return self.__f_8311800582383395327

    def __set_f_8311800582383395327(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_8311800582383395327 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_4875701691136722882(self):
        return self.__f_4875701691136722882

    def __set_f_4875701691136722882(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_4875701691136722882 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_8525072872364582718 = property(__get_f_8525072872364582718,
                                     __set_f_8525072872364582718)
    f_8311800582383395327 = property(__get_f_8311800582383395327,
                                     __set_f_8311800582383395327)
    f_4875701691136722882 = property(__get_f_4875701691136722882,
                                     __set_f_4875701691136722882)


class inst_i_4164694345981782964(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_8525072872364582718: [int, 4]  # type: ignore
    __f_4778958858443013090: [datatype.uint64, 64]  # type: ignore
    __f_7551535371612946385: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_581203445514181141: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_7818271317935764546: [STRIDE_GLB, 64]  # type: ignore
    __f_1286847141543433231: [datatype.uint16, 16]  # type: ignore
    __f_5680747367202877330: [datatype.uint16, 16]  # type: ignore
    __f_4935836554158194483: [datatype.uint16, 16]  # type: ignore
    __f_4003207286705832500: [datatype.uint16, 16]  # type: ignore
    __f_215085022235903655: [PRECISION, 2]  # type: ignore
    __f_1770559390771253019: [QUAN_SIGNED, 1]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int, int, ADDR_GLB_8_WITH_BANK,
                               ADDR_GLB_8_WITH_BANK, STRIDE_GLB, int, int, int,
                               int, PRECISION, QUAN_SIGNED,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(7)

        self.__f_1770559390771253019 = QUAN_SIGNED(0)
        cf_str += '>u1'
        self.__f_215085022235903655 = PRECISION(0)
        cf_str += '>u2'
        self.__f_4003207286705832500 = int(0)
        cf_str += '>u16'
        self.__f_4935836554158194483 = int(0)
        cf_str += '>u16'
        self.__f_5680747367202877330 = int(0)
        cf_str += '>u16'
        self.__f_1286847141543433231 = int(0)
        cf_str += '>u16'
        self.__f_7818271317935764546 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_581203445514181141 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_7551535371612946385 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_4778958858443013090 = int(0)
        cf_str += '>u64'
        self.__f_8525072872364582718 = int(0)
        cf_str += '>u4'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(75)

    def fields(
        self,
        f_8525072872364582718: int = None,
        f_4778958858443013090: int = None,
        f_7551535371612946385: ADDR_GLB_8_WITH_BANK = None,
        f_581203445514181141: ADDR_GLB_8_WITH_BANK = None,
        f_7818271317935764546: STRIDE_GLB = None,
        f_1286847141543433231: int = None,
        f_5680747367202877330: int = None,
        f_4935836554158194483: int = None,
        f_4003207286705832500: int = None,
        f_215085022235903655: PRECISION = None,
        f_1770559390771253019: QUAN_SIGNED = None,
    ):
        if f_8525072872364582718:
            self.f_8525072872364582718 = f_8525072872364582718
        if f_4778958858443013090:
            self.f_4778958858443013090 = f_4778958858443013090
        if f_7551535371612946385:
            self.f_7551535371612946385 = f_7551535371612946385
        if f_581203445514181141:
            self.f_581203445514181141 = f_581203445514181141
        if f_7818271317935764546:
            self.f_7818271317935764546 = f_7818271317935764546
        if f_1286847141543433231:
            self.f_1286847141543433231 = f_1286847141543433231
        if f_5680747367202877330:
            self.f_5680747367202877330 = f_5680747367202877330
        if f_4935836554158194483:
            self.f_4935836554158194483 = f_4935836554158194483
        if f_4003207286705832500:
            self.f_4003207286705832500 = f_4003207286705832500
        if f_215085022235903655:
            self.f_215085022235903655 = f_215085022235903655
        if f_1770559390771253019:
            self.f_1770559390771253019 = f_1770559390771253019
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_1770559390771253019),
            int(self.f_215085022235903655),
            int(self.f_4003207286705832500),
            int(self.f_4935836554158194483),
            int(self.f_5680747367202877330),
            int(self.f_1286847141543433231),
            int(self.f_7818271317935764546),
            int(self.f_581203445514181141),
            int(self.f_7551535371612946385),
            int(self.f_4778958858443013090),
            int(self.f_8525072872364582718),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 33
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x4b
        (
            self.f_1770559390771253019,
            self.f_215085022235903655,
            self.f_4003207286705832500,
            self.f_4935836554158194483,
            self.f_5680747367202877330,
            self.f_1286847141543433231,
            self.f_7818271317935764546,
            self.f_581203445514181141,
            self.f_7551535371612946385,
            self.f_4778958858443013090,
            self.f_8525072872364582718,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_4164694345981782964(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_4164694345981782964().fields(\n'
        res += '\tf_8525072872364582718 = %s ,\n' % str(
            self.f_8525072872364582718)
        res += '\tf_4778958858443013090 = %s ,\n' % str(
            self.f_4778958858443013090)
        res += '\tf_7551535371612946385 = %s ,\n' % str(
            self.f_7551535371612946385)
        res += '\tf_581203445514181141 = %s ,\n' % str(
            self.f_581203445514181141)
        res += '\tf_7818271317935764546 = %s ,\n' % str(
            self.f_7818271317935764546)
        res += '\tf_1286847141543433231 = %s ,\n' % str(
            self.f_1286847141543433231)
        res += '\tf_5680747367202877330 = %s ,\n' % str(
            self.f_5680747367202877330)
        res += '\tf_4935836554158194483 = %s ,\n' % str(
            self.f_4935836554158194483)
        res += '\tf_4003207286705832500 = %s ,\n' % str(
            self.f_4003207286705832500)
        res += '\tf_215085022235903655 = %s ,\n' % str(
            self.f_215085022235903655)
        res += '\tf_1770559390771253019 = %s ,\n' % str(
            self.f_1770559390771253019)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 33

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_8525072872364582718(self):
        return self.__f_8525072872364582718

    def __set_f_8525072872364582718(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_8525072872364582718 = int(value)

    def __get_f_4778958858443013090(self):
        return self.__f_4778958858443013090

    def __set_f_4778958858443013090(self, value):
        assert int(value) < 2**64

        assert int(value) >= 0

        self.__f_4778958858443013090 = int(value)

    def __get_f_7551535371612946385(self):
        return self.__f_7551535371612946385

    def __set_f_7551535371612946385(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_7551535371612946385 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_581203445514181141(self):
        return self.__f_581203445514181141

    def __set_f_581203445514181141(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_581203445514181141 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_7818271317935764546(self):
        return self.__f_7818271317935764546

    def __set_f_7818271317935764546(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_7818271317935764546 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_1286847141543433231(self):
        return self.__f_1286847141543433231

    def __set_f_1286847141543433231(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1286847141543433231 = int(value)

    def __get_f_5680747367202877330(self):
        return self.__f_5680747367202877330

    def __set_f_5680747367202877330(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_5680747367202877330 = int(value)

    def __get_f_4935836554158194483(self):
        return self.__f_4935836554158194483

    def __set_f_4935836554158194483(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_4935836554158194483 = int(value)

    def __get_f_4003207286705832500(self):
        return self.__f_4003207286705832500

    def __set_f_4003207286705832500(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_4003207286705832500 = int(value)

    def __get_f_215085022235903655(self):
        return self.__f_215085022235903655

    def __set_f_215085022235903655(self, value):

        assert (isinstance(value, (int, PRECISION)))
        self.__f_215085022235903655 = value if isinstance(
            value, PRECISION) else PRECISION(value)

    def __get_f_1770559390771253019(self):
        return self.__f_1770559390771253019

    def __set_f_1770559390771253019(self, value):

        assert (isinstance(value, (int, QUAN_SIGNED)))
        self.__f_1770559390771253019 = value if isinstance(
            value, QUAN_SIGNED) else QUAN_SIGNED(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_8525072872364582718 = property(__get_f_8525072872364582718,
                                     __set_f_8525072872364582718)
    f_4778958858443013090 = property(__get_f_4778958858443013090,
                                     __set_f_4778958858443013090)
    f_7551535371612946385 = property(__get_f_7551535371612946385,
                                     __set_f_7551535371612946385)
    f_581203445514181141 = property(__get_f_581203445514181141,
                                    __set_f_581203445514181141)
    f_7818271317935764546 = property(__get_f_7818271317935764546,
                                     __set_f_7818271317935764546)
    f_1286847141543433231 = property(__get_f_1286847141543433231,
                                     __set_f_1286847141543433231)
    f_5680747367202877330 = property(__get_f_5680747367202877330,
                                     __set_f_5680747367202877330)
    f_4935836554158194483 = property(__get_f_4935836554158194483,
                                     __set_f_4935836554158194483)
    f_4003207286705832500 = property(__get_f_4003207286705832500,
                                     __set_f_4003207286705832500)
    f_215085022235903655 = property(__get_f_215085022235903655,
                                    __set_f_215085022235903655)
    f_1770559390771253019 = property(__get_f_1770559390771253019,
                                     __set_f_1770559390771253019)


class inst_i_4473276217691097372(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_7480292936423069789: [CCRCLR, 8]  # type: ignore
    __f_8525072872364582718: [int, 4]  # type: ignore
    __f_3186620799393828605: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, int, ADDR_GLB_8_WITH_BANK,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(3)

        self.__f_3186620799393828605 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_8525072872364582718 = int(0)
        cf_str += '>u4'
        self.__f_7480292936423069789 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(76)

    def fields(
        self,
        f_7480292936423069789: CCRCLR = None,
        f_8525072872364582718: int = None,
        f_3186620799393828605: ADDR_GLB_8_WITH_BANK = None,
    ):
        if f_7480292936423069789:
            self.f_7480292936423069789 = f_7480292936423069789
        if f_8525072872364582718:
            self.f_8525072872364582718 = f_8525072872364582718
        if f_3186620799393828605:
            self.f_3186620799393828605 = f_3186620799393828605
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_3186620799393828605),
            int(self.f_8525072872364582718),
            int(self.f_7480292936423069789),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 6
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x4c
        (
            self.f_3186620799393828605,
            self.f_8525072872364582718,
            self.f_7480292936423069789,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_4473276217691097372(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_4473276217691097372().fields(\n'
        res += '\tf_7480292936423069789 = %s ,\n' % str(
            self.f_7480292936423069789)
        res += '\tf_8525072872364582718 = %s ,\n' % str(
            self.f_8525072872364582718)
        res += '\tf_3186620799393828605 = %s ,\n' % str(
            self.f_3186620799393828605)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 6

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_7480292936423069789(self):
        return self.__f_7480292936423069789

    def __set_f_7480292936423069789(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_7480292936423069789 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_8525072872364582718(self):
        return self.__f_8525072872364582718

    def __set_f_8525072872364582718(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_8525072872364582718 = int(value)

    def __get_f_3186620799393828605(self):
        return self.__f_3186620799393828605

    def __set_f_3186620799393828605(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_3186620799393828605 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_7480292936423069789 = property(__get_f_7480292936423069789,
                                     __set_f_7480292936423069789)
    f_8525072872364582718 = property(__get_f_8525072872364582718,
                                     __set_f_8525072872364582718)
    f_3186620799393828605 = property(__get_f_3186620799393828605,
                                     __set_f_3186620799393828605)


class inst_i_4137136459015411447(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_5647513025997157750: [CCRCLR, 8]  # type: ignore
    __f_8525072872364582718: [int, 4]  # type: ignore
    __f_6431237292802238886: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, int, ADDR_GLB_8_WITH_BANK,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(3)

        self.__f_6431237292802238886 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_8525072872364582718 = int(0)
        cf_str += '>u4'
        self.__f_5647513025997157750 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(77)

    def fields(
        self,
        f_5647513025997157750: CCRCLR = None,
        f_8525072872364582718: int = None,
        f_6431237292802238886: ADDR_GLB_8_WITH_BANK = None,
    ):
        if f_5647513025997157750:
            self.f_5647513025997157750 = f_5647513025997157750
        if f_8525072872364582718:
            self.f_8525072872364582718 = f_8525072872364582718
        if f_6431237292802238886:
            self.f_6431237292802238886 = f_6431237292802238886
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_6431237292802238886),
            int(self.f_8525072872364582718),
            int(self.f_5647513025997157750),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 6
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x4d
        (
            self.f_6431237292802238886,
            self.f_8525072872364582718,
            self.f_5647513025997157750,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_4137136459015411447(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_4137136459015411447().fields(\n'
        res += '\tf_5647513025997157750 = %s ,\n' % str(
            self.f_5647513025997157750)
        res += '\tf_8525072872364582718 = %s ,\n' % str(
            self.f_8525072872364582718)
        res += '\tf_6431237292802238886 = %s ,\n' % str(
            self.f_6431237292802238886)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 6

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_5647513025997157750(self):
        return self.__f_5647513025997157750

    def __set_f_5647513025997157750(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_5647513025997157750 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_8525072872364582718(self):
        return self.__f_8525072872364582718

    def __set_f_8525072872364582718(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_8525072872364582718 = int(value)

    def __get_f_6431237292802238886(self):
        return self.__f_6431237292802238886

    def __set_f_6431237292802238886(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_6431237292802238886 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_5647513025997157750 = property(__get_f_5647513025997157750,
                                     __set_f_5647513025997157750)
    f_8525072872364582718 = property(__get_f_8525072872364582718,
                                     __set_f_8525072872364582718)
    f_6431237292802238886 = property(__get_f_6431237292802238886,
                                     __set_f_6431237292802238886)


class inst_i_214212455253550760(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_8175951596209014998: [CCRCLR, 8]  # type: ignore
    __f_2871215043598640192: [CCRCLR, 8]  # type: ignore
    __f_1851582658599760477: [CCRSET, 11]  # type: ignore
    __f_8525072872364582718: [int, 4]  # type: ignore
    __f_2988226083445662793: [int, 1]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, CCRCLR, CCRSET, int, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        self.__f_2988226083445662793 = int(0)
        cf_str += '>u1'
        self.__f_8525072872364582718 = int(0)
        cf_str += '>u4'
        self.__f_1851582658599760477 = CCRSET(0)
        cf_str += '>u11'
        self.__f_2871215043598640192 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_8175951596209014998 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(79)

    def fields(
        self,
        f_8175951596209014998: CCRCLR = None,
        f_2871215043598640192: CCRCLR = None,
        f_1851582658599760477: CCRSET = None,
        f_8525072872364582718: int = None,
        f_2988226083445662793: int = None,
    ):
        if f_8175951596209014998:
            self.f_8175951596209014998 = f_8175951596209014998
        if f_2871215043598640192:
            self.f_2871215043598640192 = f_2871215043598640192
        if f_1851582658599760477:
            self.f_1851582658599760477 = f_1851582658599760477
        if f_8525072872364582718:
            self.f_8525072872364582718 = f_8525072872364582718
        if f_2988226083445662793:
            self.f_2988226083445662793 = f_2988226083445662793
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_2988226083445662793),
            int(self.f_8525072872364582718),
            int(self.f_1851582658599760477),
            int(self.f_2871215043598640192),
            int(self.f_8175951596209014998),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 5
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x4f
        (
            self.f_2988226083445662793,
            self.f_8525072872364582718,
            self.f_1851582658599760477,
            self.f_2871215043598640192,
            self.f_8175951596209014998,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_214212455253550760(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_214212455253550760().fields(\n'
        res += '\tf_8175951596209014998 = %s ,\n' % str(
            self.f_8175951596209014998)
        res += '\tf_2871215043598640192 = %s ,\n' % str(
            self.f_2871215043598640192)
        res += '\tf_1851582658599760477 = %s ,\n' % str(
            self.f_1851582658599760477)
        res += '\tf_8525072872364582718 = %s ,\n' % str(
            self.f_8525072872364582718)
        res += '\tf_2988226083445662793 = %s ,\n' % str(
            self.f_2988226083445662793)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 5

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_8175951596209014998(self):
        return self.__f_8175951596209014998

    def __set_f_8175951596209014998(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_8175951596209014998 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_2871215043598640192(self):
        return self.__f_2871215043598640192

    def __set_f_2871215043598640192(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_2871215043598640192 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1851582658599760477(self):
        return self.__f_1851582658599760477

    def __set_f_1851582658599760477(self, value):

        assert (isinstance(value, (int, CCRSET)))
        self.__f_1851582658599760477 = value if isinstance(
            value, CCRSET) else CCRSET(value)

    def __get_f_8525072872364582718(self):
        return self.__f_8525072872364582718

    def __set_f_8525072872364582718(self, value):
        assert int(value) < 2**4

        assert int(value) >= 0

        self.__f_8525072872364582718 = int(value)

    def __get_f_2988226083445662793(self):
        return self.__f_2988226083445662793

    def __set_f_2988226083445662793(self, value):
        assert int(value) < 2**1

        assert int(value) >= 0

        self.__f_2988226083445662793 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_8175951596209014998 = property(__get_f_8175951596209014998,
                                     __set_f_8175951596209014998)
    f_2871215043598640192 = property(__get_f_2871215043598640192,
                                     __set_f_2871215043598640192)
    f_1851582658599760477 = property(__get_f_1851582658599760477,
                                     __set_f_1851582658599760477)
    f_8525072872364582718 = property(__get_f_8525072872364582718,
                                     __set_f_8525072872364582718)
    f_2988226083445662793 = property(__get_f_2988226083445662793,
                                     __set_f_2988226083445662793)


class inst_i_7571105850837497638(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_6920772091196212887: [CCRCLR, 8]  # type: ignore
    __f_1851582658599760477: [CCRSET, 11]  # type: ignore
    __f_4535149732094779661: [UNION_ADDR, 32]  # type: ignore
    __f_581203445514181141: [UNION_ADDR, 32]  # type: ignore
    __f_9191315765263269885: [STRIDE_GLB, 64]  # type: ignore
    __f_6174243932487844318: [STRIDE_GLB, 64]  # type: ignore
    __f_1449988654089269400: [datatype.uint16, 16]  # type: ignore
    __f_8538332288708448876: [datatype.uint16, 16]  # type: ignore
    __f_8660001712953173509: [datatype.uint16, 16]  # type: ignore
    __f_2401380060870497267: [datatype.uint16, 16]  # type: ignore
    __f_35620397652795152: [int, 2]  # type: ignore
    __f_2754222333706735841: [int, 2]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, CCRSET, UNION_ADDR, UNION_ADDR,
                               STRIDE_GLB, STRIDE_GLB, int, int, int, int, int,
                               int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(1)

        self.__f_2754222333706735841 = int(0)
        cf_str += '>u2'
        self.__f_35620397652795152 = int(0)
        cf_str += '>u2'
        self.__f_2401380060870497267 = int(0)
        cf_str += '>u16'
        self.__f_8660001712953173509 = int(0)
        cf_str += '>u16'
        self.__f_8538332288708448876 = int(0)
        cf_str += '>u16'
        self.__f_1449988654089269400 = int(0)
        cf_str += '>u16'
        self.__f_6174243932487844318 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_9191315765263269885 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_581203445514181141 = UNION_ADDR(0)
        cf_str += '>u32'
        self.__f_4535149732094779661 = UNION_ADDR(0)
        cf_str += '>u32'
        self.__f_1851582658599760477 = CCRSET(0)
        cf_str += '>u11'
        self.__f_6920772091196212887 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(129)

    def fields(
        self,
        f_6920772091196212887: CCRCLR = None,
        f_1851582658599760477: CCRSET = None,
        f_4535149732094779661: UNION_ADDR = None,
        f_581203445514181141: UNION_ADDR = None,
        f_9191315765263269885: STRIDE_GLB = None,
        f_6174243932487844318: STRIDE_GLB = None,
        f_1449988654089269400: int = None,
        f_8538332288708448876: int = None,
        f_8660001712953173509: int = None,
        f_2401380060870497267: int = None,
        f_35620397652795152: int = None,
        f_2754222333706735841: int = None,
    ):
        if f_6920772091196212887:
            self.f_6920772091196212887 = f_6920772091196212887
        if f_1851582658599760477:
            self.f_1851582658599760477 = f_1851582658599760477
        if f_4535149732094779661:
            self.f_4535149732094779661 = f_4535149732094779661
        if f_581203445514181141:
            self.f_581203445514181141 = f_581203445514181141
        if f_9191315765263269885:
            self.f_9191315765263269885 = f_9191315765263269885
        if f_6174243932487844318:
            self.f_6174243932487844318 = f_6174243932487844318
        if f_1449988654089269400:
            self.f_1449988654089269400 = f_1449988654089269400
        if f_8538332288708448876:
            self.f_8538332288708448876 = f_8538332288708448876
        if f_8660001712953173509:
            self.f_8660001712953173509 = f_8660001712953173509
        if f_2401380060870497267:
            self.f_2401380060870497267 = f_2401380060870497267
        if f_35620397652795152:
            self.f_35620397652795152 = f_35620397652795152
        if f_2754222333706735841:
            self.f_2754222333706735841 = f_2754222333706735841
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_2754222333706735841),
            int(self.f_35620397652795152),
            int(self.f_2401380060870497267),
            int(self.f_8660001712953173509),
            int(self.f_8538332288708448876),
            int(self.f_1449988654089269400),
            int(self.f_6174243932487844318),
            int(self.f_9191315765263269885),
            int(self.f_581203445514181141),
            int(self.f_4535149732094779661),
            int(self.f_1851582658599760477),
            int(self.f_6920772091196212887),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 36
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x81
        (
            self.f_2754222333706735841,
            self.f_35620397652795152,
            self.f_2401380060870497267,
            self.f_8660001712953173509,
            self.f_8538332288708448876,
            self.f_1449988654089269400,
            self.f_6174243932487844318,
            self.f_9191315765263269885,
            self.f_581203445514181141,
            self.f_4535149732094779661,
            self.f_1851582658599760477,
            self.f_6920772091196212887,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_7571105850837497638(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_7571105850837497638().fields(\n'
        res += '\tf_6920772091196212887 = %s ,\n' % str(
            self.f_6920772091196212887)
        res += '\tf_1851582658599760477 = %s ,\n' % str(
            self.f_1851582658599760477)
        res += '\tf_4535149732094779661 = %s ,\n' % str(
            self.f_4535149732094779661)
        res += '\tf_581203445514181141 = %s ,\n' % str(
            self.f_581203445514181141)
        res += '\tf_9191315765263269885 = %s ,\n' % str(
            self.f_9191315765263269885)
        res += '\tf_6174243932487844318 = %s ,\n' % str(
            self.f_6174243932487844318)
        res += '\tf_1449988654089269400 = %s ,\n' % str(
            self.f_1449988654089269400)
        res += '\tf_8538332288708448876 = %s ,\n' % str(
            self.f_8538332288708448876)
        res += '\tf_8660001712953173509 = %s ,\n' % str(
            self.f_8660001712953173509)
        res += '\tf_2401380060870497267 = %s ,\n' % str(
            self.f_2401380060870497267)
        res += '\tf_35620397652795152 = %s ,\n' % str(self.f_35620397652795152)
        res += '\tf_2754222333706735841 = %s ,\n' % str(
            self.f_2754222333706735841)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 36

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_6920772091196212887(self):
        return self.__f_6920772091196212887

    def __set_f_6920772091196212887(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_6920772091196212887 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1851582658599760477(self):
        return self.__f_1851582658599760477

    def __set_f_1851582658599760477(self, value):

        assert (isinstance(value, (int, CCRSET)))
        self.__f_1851582658599760477 = value if isinstance(
            value, CCRSET) else CCRSET(value)

    def __get_f_4535149732094779661(self):
        return self.__f_4535149732094779661

    def __set_f_4535149732094779661(self, value):

        assert (isinstance(value, (int, UNION_ADDR)))
        self.__f_4535149732094779661 = value if isinstance(
            value, UNION_ADDR) else UNION_ADDR(value)

    def __get_f_581203445514181141(self):
        return self.__f_581203445514181141

    def __set_f_581203445514181141(self, value):

        assert (isinstance(value, (int, UNION_ADDR)))
        self.__f_581203445514181141 = value if isinstance(
            value, UNION_ADDR) else UNION_ADDR(value)

    def __get_f_9191315765263269885(self):
        return self.__f_9191315765263269885

    def __set_f_9191315765263269885(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_9191315765263269885 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_6174243932487844318(self):
        return self.__f_6174243932487844318

    def __set_f_6174243932487844318(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_6174243932487844318 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_1449988654089269400(self):
        return self.__f_1449988654089269400

    def __set_f_1449988654089269400(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1449988654089269400 = int(value)

    def __get_f_8538332288708448876(self):
        return self.__f_8538332288708448876

    def __set_f_8538332288708448876(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8538332288708448876 = int(value)

    def __get_f_8660001712953173509(self):
        return self.__f_8660001712953173509

    def __set_f_8660001712953173509(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8660001712953173509 = int(value)

    def __get_f_2401380060870497267(self):
        return self.__f_2401380060870497267

    def __set_f_2401380060870497267(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_2401380060870497267 = int(value)

    def __get_f_35620397652795152(self):
        return self.__f_35620397652795152

    def __set_f_35620397652795152(self, value):
        assert int(value) < 2**2

        assert int(value) >= 0

        self.__f_35620397652795152 = int(value)

    def __get_f_2754222333706735841(self):
        return self.__f_2754222333706735841

    def __set_f_2754222333706735841(self, value):
        assert int(value) < 2**2

        assert int(value) >= 0

        self.__f_2754222333706735841 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_6920772091196212887 = property(__get_f_6920772091196212887,
                                     __set_f_6920772091196212887)
    f_1851582658599760477 = property(__get_f_1851582658599760477,
                                     __set_f_1851582658599760477)
    f_4535149732094779661 = property(__get_f_4535149732094779661,
                                     __set_f_4535149732094779661)
    f_581203445514181141 = property(__get_f_581203445514181141,
                                    __set_f_581203445514181141)
    f_9191315765263269885 = property(__get_f_9191315765263269885,
                                     __set_f_9191315765263269885)
    f_6174243932487844318 = property(__get_f_6174243932487844318,
                                     __set_f_6174243932487844318)
    f_1449988654089269400 = property(__get_f_1449988654089269400,
                                     __set_f_1449988654089269400)
    f_8538332288708448876 = property(__get_f_8538332288708448876,
                                     __set_f_8538332288708448876)
    f_8660001712953173509 = property(__get_f_8660001712953173509,
                                     __set_f_8660001712953173509)
    f_2401380060870497267 = property(__get_f_2401380060870497267,
                                     __set_f_2401380060870497267)
    f_35620397652795152 = property(__get_f_35620397652795152,
                                   __set_f_35620397652795152)
    f_2754222333706735841 = property(__get_f_2754222333706735841,
                                     __set_f_2754222333706735841)


class inst_i_4966324269173843223(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_6920772091196212887: [CCRCLR, 8]  # type: ignore
    __f_1851582658599760477: [CCRSET, 11]  # type: ignore
    __f_4535149732094779661: [UNION_ADDR, 32]  # type: ignore
    __f_581203445514181141: [ADDR, 32]  # type: ignore
    __f_8504158210894135380: [datatype.uint32, 32]  # type: ignore
    __f_3574584313513507677: [int, 2]  # type: ignore
    __f_2754222333706735841: [int, 2]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, CCRSET, UNION_ADDR, ADDR, int, int,
                               int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(1)

        self.__f_2754222333706735841 = int(0)
        cf_str += '>u2'
        self.__f_3574584313513507677 = int(0)
        cf_str += '>u2'
        self.__f_8504158210894135380 = int(0)
        cf_str += '>u32'
        self.__f_581203445514181141 = ADDR(0)
        cf_str += '>u32'
        self.__f_4535149732094779661 = UNION_ADDR(0)
        cf_str += '>u32'
        self.__f_1851582658599760477 = CCRSET(0)
        cf_str += '>u11'
        self.__f_6920772091196212887 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(130)

    def fields(
        self,
        f_6920772091196212887: CCRCLR = None,
        f_1851582658599760477: CCRSET = None,
        f_4535149732094779661: UNION_ADDR = None,
        f_581203445514181141: ADDR = None,
        f_8504158210894135380: int = None,
        f_3574584313513507677: int = None,
        f_2754222333706735841: int = None,
    ):
        if f_6920772091196212887:
            self.f_6920772091196212887 = f_6920772091196212887
        if f_1851582658599760477:
            self.f_1851582658599760477 = f_1851582658599760477
        if f_4535149732094779661:
            self.f_4535149732094779661 = f_4535149732094779661
        if f_581203445514181141:
            self.f_581203445514181141 = f_581203445514181141
        if f_8504158210894135380:
            self.f_8504158210894135380 = f_8504158210894135380
        if f_3574584313513507677:
            self.f_3574584313513507677 = f_3574584313513507677
        if f_2754222333706735841:
            self.f_2754222333706735841 = f_2754222333706735841
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_2754222333706735841),
            int(self.f_3574584313513507677),
            int(self.f_8504158210894135380),
            int(self.f_581203445514181141),
            int(self.f_4535149732094779661),
            int(self.f_1851582658599760477),
            int(self.f_6920772091196212887),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 16
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x82
        (
            self.f_2754222333706735841,
            self.f_3574584313513507677,
            self.f_8504158210894135380,
            self.f_581203445514181141,
            self.f_4535149732094779661,
            self.f_1851582658599760477,
            self.f_6920772091196212887,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_4966324269173843223(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_4966324269173843223().fields(\n'
        res += '\tf_6920772091196212887 = %s ,\n' % str(
            self.f_6920772091196212887)
        res += '\tf_1851582658599760477 = %s ,\n' % str(
            self.f_1851582658599760477)
        res += '\tf_4535149732094779661 = %s ,\n' % str(
            self.f_4535149732094779661)
        res += '\tf_581203445514181141 = %s ,\n' % str(
            self.f_581203445514181141)
        res += '\tf_8504158210894135380 = %s ,\n' % str(
            self.f_8504158210894135380)
        res += '\tf_3574584313513507677 = %s ,\n' % str(
            self.f_3574584313513507677)
        res += '\tf_2754222333706735841 = %s ,\n' % str(
            self.f_2754222333706735841)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 16

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_6920772091196212887(self):
        return self.__f_6920772091196212887

    def __set_f_6920772091196212887(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_6920772091196212887 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1851582658599760477(self):
        return self.__f_1851582658599760477

    def __set_f_1851582658599760477(self, value):

        assert (isinstance(value, (int, CCRSET)))
        self.__f_1851582658599760477 = value if isinstance(
            value, CCRSET) else CCRSET(value)

    def __get_f_4535149732094779661(self):
        return self.__f_4535149732094779661

    def __set_f_4535149732094779661(self, value):

        assert (isinstance(value, (int, UNION_ADDR)))
        self.__f_4535149732094779661 = value if isinstance(
            value, UNION_ADDR) else UNION_ADDR(value)

    def __get_f_581203445514181141(self):
        return self.__f_581203445514181141

    def __set_f_581203445514181141(self, value):

        assert (isinstance(value, (int, ADDR)))
        self.__f_581203445514181141 = value if isinstance(value,
                                                          ADDR) else ADDR(value)

    def __get_f_8504158210894135380(self):
        return self.__f_8504158210894135380

    def __set_f_8504158210894135380(self, value):
        assert int(value) < 2**32

        assert int(value) >= 0

        self.__f_8504158210894135380 = int(value)

    def __get_f_3574584313513507677(self):
        return self.__f_3574584313513507677

    def __set_f_3574584313513507677(self, value):
        assert int(value) < 2**2

        assert int(value) >= 0

        self.__f_3574584313513507677 = int(value)

    def __get_f_2754222333706735841(self):
        return self.__f_2754222333706735841

    def __set_f_2754222333706735841(self, value):
        assert int(value) < 2**2

        assert int(value) >= 0

        self.__f_2754222333706735841 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_6920772091196212887 = property(__get_f_6920772091196212887,
                                     __set_f_6920772091196212887)
    f_1851582658599760477 = property(__get_f_1851582658599760477,
                                     __set_f_1851582658599760477)
    f_4535149732094779661 = property(__get_f_4535149732094779661,
                                     __set_f_4535149732094779661)
    f_581203445514181141 = property(__get_f_581203445514181141,
                                    __set_f_581203445514181141)
    f_8504158210894135380 = property(__get_f_8504158210894135380,
                                     __set_f_8504158210894135380)
    f_3574584313513507677 = property(__get_f_3574584313513507677,
                                     __set_f_3574584313513507677)
    f_2754222333706735841 = property(__get_f_2754222333706735841,
                                     __set_f_2754222333706735841)


class inst_i_6096737859014398957(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_6920772091196212887: [CCRCLR, 8]  # type: ignore
    __f_1851582658599760477: [CCRSET, 11]  # type: ignore
    __f_4535149732094779661: [UNION_ADDR, 32]  # type: ignore
    __f_581203445514181141: [UNION_ADDR, 32]  # type: ignore
    __f_8789113014547126505: [datatype.uint16, 16]  # type: ignore
    __f_9191315765263269885: [STRIDE_GLB, 64]  # type: ignore
    __f_1449988654089269400: [datatype.uint16, 16]  # type: ignore
    __f_8538332288708448876: [datatype.uint16, 16]  # type: ignore
    __f_8660001712953173509: [datatype.uint16, 16]  # type: ignore
    __f_2401380060870497267: [datatype.uint16, 16]  # type: ignore
    __f_3792019441195975024: [MFU_REDUCE_OP, 3]  # type: ignore
    __f_3299425290934234085: [MFU_REDUCE_DIM, 2]  # type: ignore
    __f_3574584313513507677: [int, 2]  # type: ignore
    __f_2754222333706735841: [int, 2]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, CCRSET, UNION_ADDR, UNION_ADDR, int,
                               STRIDE_GLB, int, int, int, int, MFU_REDUCE_OP,
                               MFU_REDUCE_DIM, int, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(4)

        self.__f_2754222333706735841 = int(0)
        cf_str += '>u2'
        self.__f_3574584313513507677 = int(0)
        cf_str += '>u2'
        self.__f_3299425290934234085 = MFU_REDUCE_DIM(0)
        cf_str += '>u2'
        self.__f_3792019441195975024 = MFU_REDUCE_OP(0)
        cf_str += '>u3'
        self.__f_2401380060870497267 = int(0)
        cf_str += '>u16'
        self.__f_8660001712953173509 = int(0)
        cf_str += '>u16'
        self.__f_8538332288708448876 = int(0)
        cf_str += '>u16'
        self.__f_1449988654089269400 = int(0)
        cf_str += '>u16'
        self.__f_9191315765263269885 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_8789113014547126505 = int(0)
        cf_str += '>u16'
        self.__f_581203445514181141 = UNION_ADDR(0)
        cf_str += '>u32'
        self.__f_4535149732094779661 = UNION_ADDR(0)
        cf_str += '>u32'
        self.__f_1851582658599760477 = CCRSET(0)
        cf_str += '>u11'
        self.__f_6920772091196212887 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(131)

    def fields(
        self,
        f_6920772091196212887: CCRCLR = None,
        f_1851582658599760477: CCRSET = None,
        f_4535149732094779661: UNION_ADDR = None,
        f_581203445514181141: UNION_ADDR = None,
        f_8789113014547126505: int = None,
        f_9191315765263269885: STRIDE_GLB = None,
        f_1449988654089269400: int = None,
        f_8538332288708448876: int = None,
        f_8660001712953173509: int = None,
        f_2401380060870497267: int = None,
        f_3792019441195975024: MFU_REDUCE_OP = None,
        f_3299425290934234085: MFU_REDUCE_DIM = None,
        f_3574584313513507677: int = None,
        f_2754222333706735841: int = None,
    ):
        if f_6920772091196212887:
            self.f_6920772091196212887 = f_6920772091196212887
        if f_1851582658599760477:
            self.f_1851582658599760477 = f_1851582658599760477
        if f_4535149732094779661:
            self.f_4535149732094779661 = f_4535149732094779661
        if f_581203445514181141:
            self.f_581203445514181141 = f_581203445514181141
        if f_8789113014547126505:
            self.f_8789113014547126505 = f_8789113014547126505
        if f_9191315765263269885:
            self.f_9191315765263269885 = f_9191315765263269885
        if f_1449988654089269400:
            self.f_1449988654089269400 = f_1449988654089269400
        if f_8538332288708448876:
            self.f_8538332288708448876 = f_8538332288708448876
        if f_8660001712953173509:
            self.f_8660001712953173509 = f_8660001712953173509
        if f_2401380060870497267:
            self.f_2401380060870497267 = f_2401380060870497267
        if f_3792019441195975024:
            self.f_3792019441195975024 = f_3792019441195975024
        if f_3299425290934234085:
            self.f_3299425290934234085 = f_3299425290934234085
        if f_3574584313513507677:
            self.f_3574584313513507677 = f_3574584313513507677
        if f_2754222333706735841:
            self.f_2754222333706735841 = f_2754222333706735841
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_2754222333706735841),
            int(self.f_3574584313513507677),
            int(self.f_3299425290934234085),
            int(self.f_3792019441195975024),
            int(self.f_2401380060870497267),
            int(self.f_8660001712953173509),
            int(self.f_8538332288708448876),
            int(self.f_1449988654089269400),
            int(self.f_9191315765263269885),
            int(self.f_8789113014547126505),
            int(self.f_581203445514181141),
            int(self.f_4535149732094779661),
            int(self.f_1851582658599760477),
            int(self.f_6920772091196212887),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 31
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x83
        (
            self.f_2754222333706735841,
            self.f_3574584313513507677,
            self.f_3299425290934234085,
            self.f_3792019441195975024,
            self.f_2401380060870497267,
            self.f_8660001712953173509,
            self.f_8538332288708448876,
            self.f_1449988654089269400,
            self.f_9191315765263269885,
            self.f_8789113014547126505,
            self.f_581203445514181141,
            self.f_4535149732094779661,
            self.f_1851582658599760477,
            self.f_6920772091196212887,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_6096737859014398957(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_6096737859014398957().fields(\n'
        res += '\tf_6920772091196212887 = %s ,\n' % str(
            self.f_6920772091196212887)
        res += '\tf_1851582658599760477 = %s ,\n' % str(
            self.f_1851582658599760477)
        res += '\tf_4535149732094779661 = %s ,\n' % str(
            self.f_4535149732094779661)
        res += '\tf_581203445514181141 = %s ,\n' % str(
            self.f_581203445514181141)
        res += '\tf_8789113014547126505 = %s ,\n' % str(
            self.f_8789113014547126505)
        res += '\tf_9191315765263269885 = %s ,\n' % str(
            self.f_9191315765263269885)
        res += '\tf_1449988654089269400 = %s ,\n' % str(
            self.f_1449988654089269400)
        res += '\tf_8538332288708448876 = %s ,\n' % str(
            self.f_8538332288708448876)
        res += '\tf_8660001712953173509 = %s ,\n' % str(
            self.f_8660001712953173509)
        res += '\tf_2401380060870497267 = %s ,\n' % str(
            self.f_2401380060870497267)
        res += '\tf_3792019441195975024 = %s ,\n' % str(
            self.f_3792019441195975024)
        res += '\tf_3299425290934234085 = %s ,\n' % str(
            self.f_3299425290934234085)
        res += '\tf_3574584313513507677 = %s ,\n' % str(
            self.f_3574584313513507677)
        res += '\tf_2754222333706735841 = %s ,\n' % str(
            self.f_2754222333706735841)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 31

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_6920772091196212887(self):
        return self.__f_6920772091196212887

    def __set_f_6920772091196212887(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_6920772091196212887 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1851582658599760477(self):
        return self.__f_1851582658599760477

    def __set_f_1851582658599760477(self, value):

        assert (isinstance(value, (int, CCRSET)))
        self.__f_1851582658599760477 = value if isinstance(
            value, CCRSET) else CCRSET(value)

    def __get_f_4535149732094779661(self):
        return self.__f_4535149732094779661

    def __set_f_4535149732094779661(self, value):

        assert (isinstance(value, (int, UNION_ADDR)))
        self.__f_4535149732094779661 = value if isinstance(
            value, UNION_ADDR) else UNION_ADDR(value)

    def __get_f_581203445514181141(self):
        return self.__f_581203445514181141

    def __set_f_581203445514181141(self, value):

        assert (isinstance(value, (int, UNION_ADDR)))
        self.__f_581203445514181141 = value if isinstance(
            value, UNION_ADDR) else UNION_ADDR(value)

    def __get_f_8789113014547126505(self):
        return self.__f_8789113014547126505

    def __set_f_8789113014547126505(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8789113014547126505 = int(value)

    def __get_f_9191315765263269885(self):
        return self.__f_9191315765263269885

    def __set_f_9191315765263269885(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_9191315765263269885 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_1449988654089269400(self):
        return self.__f_1449988654089269400

    def __set_f_1449988654089269400(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1449988654089269400 = int(value)

    def __get_f_8538332288708448876(self):
        return self.__f_8538332288708448876

    def __set_f_8538332288708448876(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8538332288708448876 = int(value)

    def __get_f_8660001712953173509(self):
        return self.__f_8660001712953173509

    def __set_f_8660001712953173509(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8660001712953173509 = int(value)

    def __get_f_2401380060870497267(self):
        return self.__f_2401380060870497267

    def __set_f_2401380060870497267(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_2401380060870497267 = int(value)

    def __get_f_3792019441195975024(self):
        return self.__f_3792019441195975024

    def __set_f_3792019441195975024(self, value):

        assert (isinstance(value, (int, MFU_REDUCE_OP)))
        self.__f_3792019441195975024 = value if isinstance(
            value, MFU_REDUCE_OP) else MFU_REDUCE_OP(value)

    def __get_f_3299425290934234085(self):
        return self.__f_3299425290934234085

    def __set_f_3299425290934234085(self, value):

        assert (isinstance(value, (int, MFU_REDUCE_DIM)))
        self.__f_3299425290934234085 = value if isinstance(
            value, MFU_REDUCE_DIM) else MFU_REDUCE_DIM(value)

    def __get_f_3574584313513507677(self):
        return self.__f_3574584313513507677

    def __set_f_3574584313513507677(self, value):
        assert int(value) < 2**2

        assert int(value) >= 0

        self.__f_3574584313513507677 = int(value)

    def __get_f_2754222333706735841(self):
        return self.__f_2754222333706735841

    def __set_f_2754222333706735841(self, value):
        assert int(value) < 2**2

        assert int(value) >= 0

        self.__f_2754222333706735841 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_6920772091196212887 = property(__get_f_6920772091196212887,
                                     __set_f_6920772091196212887)
    f_1851582658599760477 = property(__get_f_1851582658599760477,
                                     __set_f_1851582658599760477)
    f_4535149732094779661 = property(__get_f_4535149732094779661,
                                     __set_f_4535149732094779661)
    f_581203445514181141 = property(__get_f_581203445514181141,
                                    __set_f_581203445514181141)
    f_8789113014547126505 = property(__get_f_8789113014547126505,
                                     __set_f_8789113014547126505)
    f_9191315765263269885 = property(__get_f_9191315765263269885,
                                     __set_f_9191315765263269885)
    f_1449988654089269400 = property(__get_f_1449988654089269400,
                                     __set_f_1449988654089269400)
    f_8538332288708448876 = property(__get_f_8538332288708448876,
                                     __set_f_8538332288708448876)
    f_8660001712953173509 = property(__get_f_8660001712953173509,
                                     __set_f_8660001712953173509)
    f_2401380060870497267 = property(__get_f_2401380060870497267,
                                     __set_f_2401380060870497267)
    f_3792019441195975024 = property(__get_f_3792019441195975024,
                                     __set_f_3792019441195975024)
    f_3299425290934234085 = property(__get_f_3299425290934234085,
                                     __set_f_3299425290934234085)
    f_3574584313513507677 = property(__get_f_3574584313513507677,
                                     __set_f_3574584313513507677)
    f_2754222333706735841 = property(__get_f_2754222333706735841,
                                     __set_f_2754222333706735841)


class inst_i_4266661972367639294(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_6920772091196212887: [CCRCLR, 8]  # type: ignore
    __f_1851582658599760477: [CCRSET, 11]  # type: ignore
    __f_4535149732094779661: [UNION_ADDR, 32]  # type: ignore
    __f_581203445514181141: [UNION_ADDR, 32]  # type: ignore
    __f_8789113014547126505: [datatype.uint16, 16]  # type: ignore
    __f_8504158210894135380: [datatype.uint32, 32]  # type: ignore
    __f_2766670002035609535: [datatype.uint16, 16]  # type: ignore
    __f_3792019441195975024: [MFU_REDUCE_OP, 3]  # type: ignore
    __f_3574584313513507677: [int, 2]  # type: ignore
    __f_2754222333706735841: [int, 2]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, CCRSET, UNION_ADDR, UNION_ADDR, int, int,
                               int, MFU_REDUCE_OP, int, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(6)

        self.__f_2754222333706735841 = int(0)
        cf_str += '>u2'
        self.__f_3574584313513507677 = int(0)
        cf_str += '>u2'
        self.__f_3792019441195975024 = MFU_REDUCE_OP(0)
        cf_str += '>u3'
        self.__f_2766670002035609535 = int(0)
        cf_str += '>u16'
        self.__f_8504158210894135380 = int(0)
        cf_str += '>u32'
        self.__f_8789113014547126505 = int(0)
        cf_str += '>u16'
        self.__f_581203445514181141 = UNION_ADDR(0)
        cf_str += '>u32'
        self.__f_4535149732094779661 = UNION_ADDR(0)
        cf_str += '>u32'
        self.__f_1851582658599760477 = CCRSET(0)
        cf_str += '>u11'
        self.__f_6920772091196212887 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(132)

    def fields(
        self,
        f_6920772091196212887: CCRCLR = None,
        f_1851582658599760477: CCRSET = None,
        f_4535149732094779661: UNION_ADDR = None,
        f_581203445514181141: UNION_ADDR = None,
        f_8789113014547126505: int = None,
        f_8504158210894135380: int = None,
        f_2766670002035609535: int = None,
        f_3792019441195975024: MFU_REDUCE_OP = None,
        f_3574584313513507677: int = None,
        f_2754222333706735841: int = None,
    ):
        if f_6920772091196212887:
            self.f_6920772091196212887 = f_6920772091196212887
        if f_1851582658599760477:
            self.f_1851582658599760477 = f_1851582658599760477
        if f_4535149732094779661:
            self.f_4535149732094779661 = f_4535149732094779661
        if f_581203445514181141:
            self.f_581203445514181141 = f_581203445514181141
        if f_8789113014547126505:
            self.f_8789113014547126505 = f_8789113014547126505
        if f_8504158210894135380:
            self.f_8504158210894135380 = f_8504158210894135380
        if f_2766670002035609535:
            self.f_2766670002035609535 = f_2766670002035609535
        if f_3792019441195975024:
            self.f_3792019441195975024 = f_3792019441195975024
        if f_3574584313513507677:
            self.f_3574584313513507677 = f_3574584313513507677
        if f_2754222333706735841:
            self.f_2754222333706735841 = f_2754222333706735841
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_2754222333706735841),
            int(self.f_3574584313513507677),
            int(self.f_3792019441195975024),
            int(self.f_2766670002035609535),
            int(self.f_8504158210894135380),
            int(self.f_8789113014547126505),
            int(self.f_581203445514181141),
            int(self.f_4535149732094779661),
            int(self.f_1851582658599760477),
            int(self.f_6920772091196212887),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 21
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x84
        (
            self.f_2754222333706735841,
            self.f_3574584313513507677,
            self.f_3792019441195975024,
            self.f_2766670002035609535,
            self.f_8504158210894135380,
            self.f_8789113014547126505,
            self.f_581203445514181141,
            self.f_4535149732094779661,
            self.f_1851582658599760477,
            self.f_6920772091196212887,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_4266661972367639294(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_4266661972367639294().fields(\n'
        res += '\tf_6920772091196212887 = %s ,\n' % str(
            self.f_6920772091196212887)
        res += '\tf_1851582658599760477 = %s ,\n' % str(
            self.f_1851582658599760477)
        res += '\tf_4535149732094779661 = %s ,\n' % str(
            self.f_4535149732094779661)
        res += '\tf_581203445514181141 = %s ,\n' % str(
            self.f_581203445514181141)
        res += '\tf_8789113014547126505 = %s ,\n' % str(
            self.f_8789113014547126505)
        res += '\tf_8504158210894135380 = %s ,\n' % str(
            self.f_8504158210894135380)
        res += '\tf_2766670002035609535 = %s ,\n' % str(
            self.f_2766670002035609535)
        res += '\tf_3792019441195975024 = %s ,\n' % str(
            self.f_3792019441195975024)
        res += '\tf_3574584313513507677 = %s ,\n' % str(
            self.f_3574584313513507677)
        res += '\tf_2754222333706735841 = %s ,\n' % str(
            self.f_2754222333706735841)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 21

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_6920772091196212887(self):
        return self.__f_6920772091196212887

    def __set_f_6920772091196212887(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_6920772091196212887 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1851582658599760477(self):
        return self.__f_1851582658599760477

    def __set_f_1851582658599760477(self, value):

        assert (isinstance(value, (int, CCRSET)))
        self.__f_1851582658599760477 = value if isinstance(
            value, CCRSET) else CCRSET(value)

    def __get_f_4535149732094779661(self):
        return self.__f_4535149732094779661

    def __set_f_4535149732094779661(self, value):

        assert (isinstance(value, (int, UNION_ADDR)))
        self.__f_4535149732094779661 = value if isinstance(
            value, UNION_ADDR) else UNION_ADDR(value)

    def __get_f_581203445514181141(self):
        return self.__f_581203445514181141

    def __set_f_581203445514181141(self, value):

        assert (isinstance(value, (int, UNION_ADDR)))
        self.__f_581203445514181141 = value if isinstance(
            value, UNION_ADDR) else UNION_ADDR(value)

    def __get_f_8789113014547126505(self):
        return self.__f_8789113014547126505

    def __set_f_8789113014547126505(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8789113014547126505 = int(value)

    def __get_f_8504158210894135380(self):
        return self.__f_8504158210894135380

    def __set_f_8504158210894135380(self, value):
        assert int(value) < 2**32

        assert int(value) >= 0

        self.__f_8504158210894135380 = int(value)

    def __get_f_2766670002035609535(self):
        return self.__f_2766670002035609535

    def __set_f_2766670002035609535(self, value):
        assert int(value) < 2**16

        assert int(value) > 2
        self.__f_2766670002035609535 = int(value)

    def __get_f_3792019441195975024(self):
        return self.__f_3792019441195975024

    def __set_f_3792019441195975024(self, value):

        assert (isinstance(value, (int, MFU_REDUCE_OP)))
        self.__f_3792019441195975024 = value if isinstance(
            value, MFU_REDUCE_OP) else MFU_REDUCE_OP(value)

    def __get_f_3574584313513507677(self):
        return self.__f_3574584313513507677

    def __set_f_3574584313513507677(self, value):
        assert int(value) < 2**2

        assert int(value) >= 0

        self.__f_3574584313513507677 = int(value)

    def __get_f_2754222333706735841(self):
        return self.__f_2754222333706735841

    def __set_f_2754222333706735841(self, value):
        assert int(value) < 2**2

        assert int(value) >= 0

        self.__f_2754222333706735841 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_6920772091196212887 = property(__get_f_6920772091196212887,
                                     __set_f_6920772091196212887)
    f_1851582658599760477 = property(__get_f_1851582658599760477,
                                     __set_f_1851582658599760477)
    f_4535149732094779661 = property(__get_f_4535149732094779661,
                                     __set_f_4535149732094779661)
    f_581203445514181141 = property(__get_f_581203445514181141,
                                    __set_f_581203445514181141)
    f_8789113014547126505 = property(__get_f_8789113014547126505,
                                     __set_f_8789113014547126505)
    f_8504158210894135380 = property(__get_f_8504158210894135380,
                                     __set_f_8504158210894135380)
    f_2766670002035609535 = property(__get_f_2766670002035609535,
                                     __set_f_2766670002035609535)
    f_3792019441195975024 = property(__get_f_3792019441195975024,
                                     __set_f_3792019441195975024)
    f_3574584313513507677 = property(__get_f_3574584313513507677,
                                     __set_f_3574584313513507677)
    f_2754222333706735841 = property(__get_f_2754222333706735841,
                                     __set_f_2754222333706735841)


class inst_i_1712250146653531835(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_7480292936423069789: [CCRCLR, 8]  # type: ignore
    __f_5647513025997157750: [CCRCLR, 8]  # type: ignore
    __f_1851582658599760477: [CCRSET, 11]  # type: ignore
    __f_3186620799393828605: [UNION_ADDR, 32]  # type: ignore
    __f_6431237292802238886: [UNION_ADDR, 32]  # type: ignore
    __f_581203445514181141: [UNION_ADDR, 32]  # type: ignore
    __f_317478884186617204: [datatype.uint32, 32]  # type: ignore
    __f_227249044740642424: [datatype.uint32, 32]  # type: ignore
    __f_2206373936754291286: [datatype.uint32, 32]  # type: ignore
    __f_35620397652795152: [int, 2]  # type: ignore
    __f_3712297140628946986: [int, 2]  # type: ignore
    __f_2754222333706735841: [int, 2]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, CCRCLR, CCRSET, UNION_ADDR, UNION_ADDR,
                               UNION_ADDR, int, int, int, int, int,
                               int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(7)

        self.__f_2754222333706735841 = int(0)
        cf_str += '>u2'
        self.__f_3712297140628946986 = int(0)
        cf_str += '>u2'
        self.__f_35620397652795152 = int(0)
        cf_str += '>u2'
        self.__f_2206373936754291286 = int(0)
        cf_str += '>u32'
        self.__f_227249044740642424 = int(0)
        cf_str += '>u32'
        self.__f_317478884186617204 = int(0)
        cf_str += '>u32'
        self.__f_581203445514181141 = UNION_ADDR(0)
        cf_str += '>u32'
        self.__f_6431237292802238886 = UNION_ADDR(0)
        cf_str += '>u32'
        self.__f_3186620799393828605 = UNION_ADDR(0)
        cf_str += '>u32'
        self.__f_1851582658599760477 = CCRSET(0)
        cf_str += '>u11'
        self.__f_5647513025997157750 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_7480292936423069789 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(133)

    def fields(
        self,
        f_7480292936423069789: CCRCLR = None,
        f_5647513025997157750: CCRCLR = None,
        f_1851582658599760477: CCRSET = None,
        f_3186620799393828605: UNION_ADDR = None,
        f_6431237292802238886: UNION_ADDR = None,
        f_581203445514181141: UNION_ADDR = None,
        f_317478884186617204: int = None,
        f_227249044740642424: int = None,
        f_2206373936754291286: int = None,
        f_35620397652795152: int = None,
        f_3712297140628946986: int = None,
        f_2754222333706735841: int = None,
    ):
        if f_7480292936423069789:
            self.f_7480292936423069789 = f_7480292936423069789
        if f_5647513025997157750:
            self.f_5647513025997157750 = f_5647513025997157750
        if f_1851582658599760477:
            self.f_1851582658599760477 = f_1851582658599760477
        if f_3186620799393828605:
            self.f_3186620799393828605 = f_3186620799393828605
        if f_6431237292802238886:
            self.f_6431237292802238886 = f_6431237292802238886
        if f_581203445514181141:
            self.f_581203445514181141 = f_581203445514181141
        if f_317478884186617204:
            self.f_317478884186617204 = f_317478884186617204
        if f_227249044740642424:
            self.f_227249044740642424 = f_227249044740642424
        if f_2206373936754291286:
            self.f_2206373936754291286 = f_2206373936754291286
        if f_35620397652795152:
            self.f_35620397652795152 = f_35620397652795152
        if f_3712297140628946986:
            self.f_3712297140628946986 = f_3712297140628946986
        if f_2754222333706735841:
            self.f_2754222333706735841 = f_2754222333706735841
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_2754222333706735841),
            int(self.f_3712297140628946986),
            int(self.f_35620397652795152),
            int(self.f_2206373936754291286),
            int(self.f_227249044740642424),
            int(self.f_317478884186617204),
            int(self.f_581203445514181141),
            int(self.f_6431237292802238886),
            int(self.f_3186620799393828605),
            int(self.f_1851582658599760477),
            int(self.f_5647513025997157750),
            int(self.f_7480292936423069789),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 30
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x85
        (
            self.f_2754222333706735841,
            self.f_3712297140628946986,
            self.f_35620397652795152,
            self.f_2206373936754291286,
            self.f_227249044740642424,
            self.f_317478884186617204,
            self.f_581203445514181141,
            self.f_6431237292802238886,
            self.f_3186620799393828605,
            self.f_1851582658599760477,
            self.f_5647513025997157750,
            self.f_7480292936423069789,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_1712250146653531835(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_1712250146653531835().fields(\n'
        res += '\tf_7480292936423069789 = %s ,\n' % str(
            self.f_7480292936423069789)
        res += '\tf_5647513025997157750 = %s ,\n' % str(
            self.f_5647513025997157750)
        res += '\tf_1851582658599760477 = %s ,\n' % str(
            self.f_1851582658599760477)
        res += '\tf_3186620799393828605 = %s ,\n' % str(
            self.f_3186620799393828605)
        res += '\tf_6431237292802238886 = %s ,\n' % str(
            self.f_6431237292802238886)
        res += '\tf_581203445514181141 = %s ,\n' % str(
            self.f_581203445514181141)
        res += '\tf_317478884186617204 = %s ,\n' % str(
            self.f_317478884186617204)
        res += '\tf_227249044740642424 = %s ,\n' % str(
            self.f_227249044740642424)
        res += '\tf_2206373936754291286 = %s ,\n' % str(
            self.f_2206373936754291286)
        res += '\tf_35620397652795152 = %s ,\n' % str(self.f_35620397652795152)
        res += '\tf_3712297140628946986 = %s ,\n' % str(
            self.f_3712297140628946986)
        res += '\tf_2754222333706735841 = %s ,\n' % str(
            self.f_2754222333706735841)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 30

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_7480292936423069789(self):
        return self.__f_7480292936423069789

    def __set_f_7480292936423069789(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_7480292936423069789 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_5647513025997157750(self):
        return self.__f_5647513025997157750

    def __set_f_5647513025997157750(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_5647513025997157750 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1851582658599760477(self):
        return self.__f_1851582658599760477

    def __set_f_1851582658599760477(self, value):

        assert (isinstance(value, (int, CCRSET)))
        self.__f_1851582658599760477 = value if isinstance(
            value, CCRSET) else CCRSET(value)

    def __get_f_3186620799393828605(self):
        return self.__f_3186620799393828605

    def __set_f_3186620799393828605(self, value):

        assert (isinstance(value, (int, UNION_ADDR)))
        self.__f_3186620799393828605 = value if isinstance(
            value, UNION_ADDR) else UNION_ADDR(value)

    def __get_f_6431237292802238886(self):
        return self.__f_6431237292802238886

    def __set_f_6431237292802238886(self, value):

        assert (isinstance(value, (int, UNION_ADDR)))
        self.__f_6431237292802238886 = value if isinstance(
            value, UNION_ADDR) else UNION_ADDR(value)

    def __get_f_581203445514181141(self):
        return self.__f_581203445514181141

    def __set_f_581203445514181141(self, value):

        assert (isinstance(value, (int, UNION_ADDR)))
        self.__f_581203445514181141 = value if isinstance(
            value, UNION_ADDR) else UNION_ADDR(value)

    def __get_f_317478884186617204(self):
        return self.__f_317478884186617204

    def __set_f_317478884186617204(self, value):
        assert int(value) < 2**32

        assert int(value) >= 0

        self.__f_317478884186617204 = int(value)

    def __get_f_227249044740642424(self):
        return self.__f_227249044740642424

    def __set_f_227249044740642424(self, value):
        assert int(value) < 2**32

        assert int(value) >= 0

        self.__f_227249044740642424 = int(value)

    def __get_f_2206373936754291286(self):
        return self.__f_2206373936754291286

    def __set_f_2206373936754291286(self, value):
        assert int(value) < 2**32

        assert int(value) >= 0

        self.__f_2206373936754291286 = int(value)

    def __get_f_35620397652795152(self):
        return self.__f_35620397652795152

    def __set_f_35620397652795152(self, value):
        assert int(value) < 2**2

        assert int(value) >= 0

        self.__f_35620397652795152 = int(value)

    def __get_f_3712297140628946986(self):
        return self.__f_3712297140628946986

    def __set_f_3712297140628946986(self, value):
        assert int(value) < 2**2

        assert int(value) >= 0

        self.__f_3712297140628946986 = int(value)

    def __get_f_2754222333706735841(self):
        return self.__f_2754222333706735841

    def __set_f_2754222333706735841(self, value):
        assert int(value) < 2**2

        assert int(value) >= 0

        self.__f_2754222333706735841 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_7480292936423069789 = property(__get_f_7480292936423069789,
                                     __set_f_7480292936423069789)
    f_5647513025997157750 = property(__get_f_5647513025997157750,
                                     __set_f_5647513025997157750)
    f_1851582658599760477 = property(__get_f_1851582658599760477,
                                     __set_f_1851582658599760477)
    f_3186620799393828605 = property(__get_f_3186620799393828605,
                                     __set_f_3186620799393828605)
    f_6431237292802238886 = property(__get_f_6431237292802238886,
                                     __set_f_6431237292802238886)
    f_581203445514181141 = property(__get_f_581203445514181141,
                                    __set_f_581203445514181141)
    f_317478884186617204 = property(__get_f_317478884186617204,
                                    __set_f_317478884186617204)
    f_227249044740642424 = property(__get_f_227249044740642424,
                                    __set_f_227249044740642424)
    f_2206373936754291286 = property(__get_f_2206373936754291286,
                                     __set_f_2206373936754291286)
    f_35620397652795152 = property(__get_f_35620397652795152,
                                   __set_f_35620397652795152)
    f_3712297140628946986 = property(__get_f_3712297140628946986,
                                     __set_f_3712297140628946986)
    f_2754222333706735841 = property(__get_f_2754222333706735841,
                                     __set_f_2754222333706735841)


class inst_i_447177514076795622(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_8789113014547126505: [datatype.uint16, 16]  # type: ignore
    __f_6473137396523522442: [datatype.uint16, 16]  # type: ignore
    __f_8504158210894135380: [int, 29]  # type: ignore
    __f_3792019441195975024: [MFU_REDUCE_OP, 3]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int, int, int, MFU_REDUCE_OP,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        self.__f_3792019441195975024 = MFU_REDUCE_OP(0)
        cf_str += '>u3'
        self.__f_8504158210894135380 = int(0)
        cf_str += '>u29'
        self.__f_6473137396523522442 = int(0)
        cf_str += '>u16'
        self.__f_8789113014547126505 = int(0)
        cf_str += '>u16'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(134)

    def fields(
        self,
        f_8789113014547126505: int = None,
        f_6473137396523522442: int = None,
        f_8504158210894135380: int = None,
        f_3792019441195975024: MFU_REDUCE_OP = None,
    ):
        if f_8789113014547126505:
            self.f_8789113014547126505 = f_8789113014547126505
        if f_6473137396523522442:
            self.f_6473137396523522442 = f_6473137396523522442
        if f_8504158210894135380:
            self.f_8504158210894135380 = f_8504158210894135380
        if f_3792019441195975024:
            self.f_3792019441195975024 = f_3792019441195975024
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_3792019441195975024),
            int(self.f_8504158210894135380),
            int(self.f_6473137396523522442),
            int(self.f_8789113014547126505),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 9
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x86
        (
            self.f_3792019441195975024,
            self.f_8504158210894135380,
            self.f_6473137396523522442,
            self.f_8789113014547126505,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_447177514076795622(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_447177514076795622().fields(\n'
        res += '\tf_8789113014547126505 = %s ,\n' % str(
            self.f_8789113014547126505)
        res += '\tf_6473137396523522442 = %s ,\n' % str(
            self.f_6473137396523522442)
        res += '\tf_8504158210894135380 = %s ,\n' % str(
            self.f_8504158210894135380)
        res += '\tf_3792019441195975024 = %s ,\n' % str(
            self.f_3792019441195975024)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 9

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_8789113014547126505(self):
        return self.__f_8789113014547126505

    def __set_f_8789113014547126505(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8789113014547126505 = int(value)

    def __get_f_6473137396523522442(self):
        return self.__f_6473137396523522442

    def __set_f_6473137396523522442(self, value):
        assert int(value) < 2**16

        assert int(value) > 2
        self.__f_6473137396523522442 = int(value)

    def __get_f_8504158210894135380(self):
        return self.__f_8504158210894135380

    def __set_f_8504158210894135380(self, value):
        assert int(value) < 2**29

        assert int(value) >= 0

        self.__f_8504158210894135380 = int(value)

    def __get_f_3792019441195975024(self):
        return self.__f_3792019441195975024

    def __set_f_3792019441195975024(self, value):

        assert (isinstance(value, (int, MFU_REDUCE_OP)))
        self.__f_3792019441195975024 = value if isinstance(
            value, MFU_REDUCE_OP) else MFU_REDUCE_OP(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_8789113014547126505 = property(__get_f_8789113014547126505,
                                     __set_f_8789113014547126505)
    f_6473137396523522442 = property(__get_f_6473137396523522442,
                                     __set_f_6473137396523522442)
    f_8504158210894135380 = property(__get_f_8504158210894135380,
                                     __set_f_8504158210894135380)
    f_3792019441195975024 = property(__get_f_3792019441195975024,
                                     __set_f_3792019441195975024)


class inst_i_2656964308044352142(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_9058508044500194118: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_268400827519036290: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_3804720826429252246: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_4094387588779856056: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_3722284515940164363: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_2763215685155701833: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_8809170042491063265: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_2674756877849412408: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_9151497388570990265: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_1565678452235615105: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_157333374141651885: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_235546436338242801: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_6462998562482886591: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_8779414760933169917: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_5451984308869576529: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_188855504015312136: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_6368608406811834432: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_8020340105449100677: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_3972783259428801223: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_2197059032295624775: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_7060794749477844133: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_2745652021697515536: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_6034395913105951305: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_916767987577961714: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_2966179821931253906: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_9155677745115475027: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_4136853236801857886: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_2985938125053332294: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_2164339272227203922: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_114804966380045502: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_2445336287606983664: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_7151644913908691297: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_1604490753204815046: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_3128456386189085959: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_9057435281982809915: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_1353983061390515983: [MFU_MN_PORTOUT, 6]  # type: ignore
    __f_278680869427956803: [MFU_MN_PORTOUT, 6]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[MFU_MN_PORTOUT, MFU_MN_PORTOUT, MFU_MN_PORTOUT,
                               MFU_MN_PORTOUT, MFU_MN_PORTOUT, MFU_MN_PORTOUT,
                               MFU_MN_PORTOUT, MFU_MN_PORTOUT, MFU_MN_PORTOUT,
                               MFU_MN_PORTOUT, MFU_MN_PORTOUT, MFU_MN_PORTOUT,
                               MFU_MN_PORTOUT, MFU_MN_PORTOUT, MFU_MN_PORTOUT,
                               MFU_MN_PORTOUT, MFU_MN_PORTOUT, MFU_MN_PORTOUT,
                               MFU_MN_PORTOUT, MFU_MN_PORTOUT, MFU_MN_PORTOUT,
                               MFU_MN_PORTOUT, MFU_MN_PORTOUT, MFU_MN_PORTOUT,
                               MFU_MN_PORTOUT, MFU_MN_PORTOUT, MFU_MN_PORTOUT,
                               MFU_MN_PORTOUT, MFU_MN_PORTOUT, MFU_MN_PORTOUT,
                               MFU_MN_PORTOUT, MFU_MN_PORTOUT, MFU_MN_PORTOUT,
                               MFU_MN_PORTOUT, MFU_MN_PORTOUT, MFU_MN_PORTOUT,
                               MFU_MN_PORTOUT,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(2)

        self.__f_278680869427956803 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_1353983061390515983 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_9057435281982809915 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_3128456386189085959 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_1604490753204815046 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_7151644913908691297 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_2445336287606983664 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_114804966380045502 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_2164339272227203922 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_2985938125053332294 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_4136853236801857886 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_9155677745115475027 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_2966179821931253906 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_916767987577961714 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_6034395913105951305 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_2745652021697515536 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_7060794749477844133 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_2197059032295624775 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_3972783259428801223 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_8020340105449100677 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_6368608406811834432 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_188855504015312136 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_5451984308869576529 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_8779414760933169917 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_6462998562482886591 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_235546436338242801 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_157333374141651885 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_1565678452235615105 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_9151497388570990265 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_2674756877849412408 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_8809170042491063265 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_2763215685155701833 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_3722284515940164363 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_4094387588779856056 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_3804720826429252246 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_268400827519036290 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_9058508044500194118 = MFU_MN_PORTOUT(0)
        cf_str += '>u6'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(135)

    def fields(
        self,
        f_9058508044500194118: MFU_MN_PORTOUT = None,
        f_268400827519036290: MFU_MN_PORTOUT = None,
        f_3804720826429252246: MFU_MN_PORTOUT = None,
        f_4094387588779856056: MFU_MN_PORTOUT = None,
        f_3722284515940164363: MFU_MN_PORTOUT = None,
        f_2763215685155701833: MFU_MN_PORTOUT = None,
        f_8809170042491063265: MFU_MN_PORTOUT = None,
        f_2674756877849412408: MFU_MN_PORTOUT = None,
        f_9151497388570990265: MFU_MN_PORTOUT = None,
        f_1565678452235615105: MFU_MN_PORTOUT = None,
        f_157333374141651885: MFU_MN_PORTOUT = None,
        f_235546436338242801: MFU_MN_PORTOUT = None,
        f_6462998562482886591: MFU_MN_PORTOUT = None,
        f_8779414760933169917: MFU_MN_PORTOUT = None,
        f_5451984308869576529: MFU_MN_PORTOUT = None,
        f_188855504015312136: MFU_MN_PORTOUT = None,
        f_6368608406811834432: MFU_MN_PORTOUT = None,
        f_8020340105449100677: MFU_MN_PORTOUT = None,
        f_3972783259428801223: MFU_MN_PORTOUT = None,
        f_2197059032295624775: MFU_MN_PORTOUT = None,
        f_7060794749477844133: MFU_MN_PORTOUT = None,
        f_2745652021697515536: MFU_MN_PORTOUT = None,
        f_6034395913105951305: MFU_MN_PORTOUT = None,
        f_916767987577961714: MFU_MN_PORTOUT = None,
        f_2966179821931253906: MFU_MN_PORTOUT = None,
        f_9155677745115475027: MFU_MN_PORTOUT = None,
        f_4136853236801857886: MFU_MN_PORTOUT = None,
        f_2985938125053332294: MFU_MN_PORTOUT = None,
        f_2164339272227203922: MFU_MN_PORTOUT = None,
        f_114804966380045502: MFU_MN_PORTOUT = None,
        f_2445336287606983664: MFU_MN_PORTOUT = None,
        f_7151644913908691297: MFU_MN_PORTOUT = None,
        f_1604490753204815046: MFU_MN_PORTOUT = None,
        f_3128456386189085959: MFU_MN_PORTOUT = None,
        f_9057435281982809915: MFU_MN_PORTOUT = None,
        f_1353983061390515983: MFU_MN_PORTOUT = None,
        f_278680869427956803: MFU_MN_PORTOUT = None,
    ):
        if f_9058508044500194118:
            self.f_9058508044500194118 = f_9058508044500194118
        if f_268400827519036290:
            self.f_268400827519036290 = f_268400827519036290
        if f_3804720826429252246:
            self.f_3804720826429252246 = f_3804720826429252246
        if f_4094387588779856056:
            self.f_4094387588779856056 = f_4094387588779856056
        if f_3722284515940164363:
            self.f_3722284515940164363 = f_3722284515940164363
        if f_2763215685155701833:
            self.f_2763215685155701833 = f_2763215685155701833
        if f_8809170042491063265:
            self.f_8809170042491063265 = f_8809170042491063265
        if f_2674756877849412408:
            self.f_2674756877849412408 = f_2674756877849412408
        if f_9151497388570990265:
            self.f_9151497388570990265 = f_9151497388570990265
        if f_1565678452235615105:
            self.f_1565678452235615105 = f_1565678452235615105
        if f_157333374141651885:
            self.f_157333374141651885 = f_157333374141651885
        if f_235546436338242801:
            self.f_235546436338242801 = f_235546436338242801
        if f_6462998562482886591:
            self.f_6462998562482886591 = f_6462998562482886591
        if f_8779414760933169917:
            self.f_8779414760933169917 = f_8779414760933169917
        if f_5451984308869576529:
            self.f_5451984308869576529 = f_5451984308869576529
        if f_188855504015312136:
            self.f_188855504015312136 = f_188855504015312136
        if f_6368608406811834432:
            self.f_6368608406811834432 = f_6368608406811834432
        if f_8020340105449100677:
            self.f_8020340105449100677 = f_8020340105449100677
        if f_3972783259428801223:
            self.f_3972783259428801223 = f_3972783259428801223
        if f_2197059032295624775:
            self.f_2197059032295624775 = f_2197059032295624775
        if f_7060794749477844133:
            self.f_7060794749477844133 = f_7060794749477844133
        if f_2745652021697515536:
            self.f_2745652021697515536 = f_2745652021697515536
        if f_6034395913105951305:
            self.f_6034395913105951305 = f_6034395913105951305
        if f_916767987577961714:
            self.f_916767987577961714 = f_916767987577961714
        if f_2966179821931253906:
            self.f_2966179821931253906 = f_2966179821931253906
        if f_9155677745115475027:
            self.f_9155677745115475027 = f_9155677745115475027
        if f_4136853236801857886:
            self.f_4136853236801857886 = f_4136853236801857886
        if f_2985938125053332294:
            self.f_2985938125053332294 = f_2985938125053332294
        if f_2164339272227203922:
            self.f_2164339272227203922 = f_2164339272227203922
        if f_114804966380045502:
            self.f_114804966380045502 = f_114804966380045502
        if f_2445336287606983664:
            self.f_2445336287606983664 = f_2445336287606983664
        if f_7151644913908691297:
            self.f_7151644913908691297 = f_7151644913908691297
        if f_1604490753204815046:
            self.f_1604490753204815046 = f_1604490753204815046
        if f_3128456386189085959:
            self.f_3128456386189085959 = f_3128456386189085959
        if f_9057435281982809915:
            self.f_9057435281982809915 = f_9057435281982809915
        if f_1353983061390515983:
            self.f_1353983061390515983 = f_1353983061390515983
        if f_278680869427956803:
            self.f_278680869427956803 = f_278680869427956803
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_278680869427956803),
            int(self.f_1353983061390515983),
            int(self.f_9057435281982809915),
            int(self.f_3128456386189085959),
            int(self.f_1604490753204815046),
            int(self.f_7151644913908691297),
            int(self.f_2445336287606983664),
            int(self.f_114804966380045502),
            int(self.f_2164339272227203922),
            int(self.f_2985938125053332294),
            int(self.f_4136853236801857886),
            int(self.f_9155677745115475027),
            int(self.f_2966179821931253906),
            int(self.f_916767987577961714),
            int(self.f_6034395913105951305),
            int(self.f_2745652021697515536),
            int(self.f_7060794749477844133),
            int(self.f_2197059032295624775),
            int(self.f_3972783259428801223),
            int(self.f_8020340105449100677),
            int(self.f_6368608406811834432),
            int(self.f_188855504015312136),
            int(self.f_5451984308869576529),
            int(self.f_8779414760933169917),
            int(self.f_6462998562482886591),
            int(self.f_235546436338242801),
            int(self.f_157333374141651885),
            int(self.f_1565678452235615105),
            int(self.f_9151497388570990265),
            int(self.f_2674756877849412408),
            int(self.f_8809170042491063265),
            int(self.f_2763215685155701833),
            int(self.f_3722284515940164363),
            int(self.f_4094387588779856056),
            int(self.f_3804720826429252246),
            int(self.f_268400827519036290),
            int(self.f_9058508044500194118),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 29
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x87
        (
            self.f_278680869427956803,
            self.f_1353983061390515983,
            self.f_9057435281982809915,
            self.f_3128456386189085959,
            self.f_1604490753204815046,
            self.f_7151644913908691297,
            self.f_2445336287606983664,
            self.f_114804966380045502,
            self.f_2164339272227203922,
            self.f_2985938125053332294,
            self.f_4136853236801857886,
            self.f_9155677745115475027,
            self.f_2966179821931253906,
            self.f_916767987577961714,
            self.f_6034395913105951305,
            self.f_2745652021697515536,
            self.f_7060794749477844133,
            self.f_2197059032295624775,
            self.f_3972783259428801223,
            self.f_8020340105449100677,
            self.f_6368608406811834432,
            self.f_188855504015312136,
            self.f_5451984308869576529,
            self.f_8779414760933169917,
            self.f_6462998562482886591,
            self.f_235546436338242801,
            self.f_157333374141651885,
            self.f_1565678452235615105,
            self.f_9151497388570990265,
            self.f_2674756877849412408,
            self.f_8809170042491063265,
            self.f_2763215685155701833,
            self.f_3722284515940164363,
            self.f_4094387588779856056,
            self.f_3804720826429252246,
            self.f_268400827519036290,
            self.f_9058508044500194118,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_2656964308044352142(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_2656964308044352142().fields(\n'
        res += '\tf_9058508044500194118 = %s ,\n' % str(
            self.f_9058508044500194118)
        res += '\tf_268400827519036290 = %s ,\n' % str(
            self.f_268400827519036290)
        res += '\tf_3804720826429252246 = %s ,\n' % str(
            self.f_3804720826429252246)
        res += '\tf_4094387588779856056 = %s ,\n' % str(
            self.f_4094387588779856056)
        res += '\tf_3722284515940164363 = %s ,\n' % str(
            self.f_3722284515940164363)
        res += '\tf_2763215685155701833 = %s ,\n' % str(
            self.f_2763215685155701833)
        res += '\tf_8809170042491063265 = %s ,\n' % str(
            self.f_8809170042491063265)
        res += '\tf_2674756877849412408 = %s ,\n' % str(
            self.f_2674756877849412408)
        res += '\tf_9151497388570990265 = %s ,\n' % str(
            self.f_9151497388570990265)
        res += '\tf_1565678452235615105 = %s ,\n' % str(
            self.f_1565678452235615105)
        res += '\tf_157333374141651885 = %s ,\n' % str(
            self.f_157333374141651885)
        res += '\tf_235546436338242801 = %s ,\n' % str(
            self.f_235546436338242801)
        res += '\tf_6462998562482886591 = %s ,\n' % str(
            self.f_6462998562482886591)
        res += '\tf_8779414760933169917 = %s ,\n' % str(
            self.f_8779414760933169917)
        res += '\tf_5451984308869576529 = %s ,\n' % str(
            self.f_5451984308869576529)
        res += '\tf_188855504015312136 = %s ,\n' % str(
            self.f_188855504015312136)
        res += '\tf_6368608406811834432 = %s ,\n' % str(
            self.f_6368608406811834432)
        res += '\tf_8020340105449100677 = %s ,\n' % str(
            self.f_8020340105449100677)
        res += '\tf_3972783259428801223 = %s ,\n' % str(
            self.f_3972783259428801223)
        res += '\tf_2197059032295624775 = %s ,\n' % str(
            self.f_2197059032295624775)
        res += '\tf_7060794749477844133 = %s ,\n' % str(
            self.f_7060794749477844133)
        res += '\tf_2745652021697515536 = %s ,\n' % str(
            self.f_2745652021697515536)
        res += '\tf_6034395913105951305 = %s ,\n' % str(
            self.f_6034395913105951305)
        res += '\tf_916767987577961714 = %s ,\n' % str(
            self.f_916767987577961714)
        res += '\tf_2966179821931253906 = %s ,\n' % str(
            self.f_2966179821931253906)
        res += '\tf_9155677745115475027 = %s ,\n' % str(
            self.f_9155677745115475027)
        res += '\tf_4136853236801857886 = %s ,\n' % str(
            self.f_4136853236801857886)
        res += '\tf_2985938125053332294 = %s ,\n' % str(
            self.f_2985938125053332294)
        res += '\tf_2164339272227203922 = %s ,\n' % str(
            self.f_2164339272227203922)
        res += '\tf_114804966380045502 = %s ,\n' % str(
            self.f_114804966380045502)
        res += '\tf_2445336287606983664 = %s ,\n' % str(
            self.f_2445336287606983664)
        res += '\tf_7151644913908691297 = %s ,\n' % str(
            self.f_7151644913908691297)
        res += '\tf_1604490753204815046 = %s ,\n' % str(
            self.f_1604490753204815046)
        res += '\tf_3128456386189085959 = %s ,\n' % str(
            self.f_3128456386189085959)
        res += '\tf_9057435281982809915 = %s ,\n' % str(
            self.f_9057435281982809915)
        res += '\tf_1353983061390515983 = %s ,\n' % str(
            self.f_1353983061390515983)
        res += '\tf_278680869427956803 = %s ,\n' % str(
            self.f_278680869427956803)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 29

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_9058508044500194118(self):
        return self.__f_9058508044500194118

    def __set_f_9058508044500194118(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_9058508044500194118 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_268400827519036290(self):
        return self.__f_268400827519036290

    def __set_f_268400827519036290(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_268400827519036290 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_3804720826429252246(self):
        return self.__f_3804720826429252246

    def __set_f_3804720826429252246(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_3804720826429252246 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_4094387588779856056(self):
        return self.__f_4094387588779856056

    def __set_f_4094387588779856056(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_4094387588779856056 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_3722284515940164363(self):
        return self.__f_3722284515940164363

    def __set_f_3722284515940164363(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_3722284515940164363 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_2763215685155701833(self):
        return self.__f_2763215685155701833

    def __set_f_2763215685155701833(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_2763215685155701833 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_8809170042491063265(self):
        return self.__f_8809170042491063265

    def __set_f_8809170042491063265(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_8809170042491063265 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_2674756877849412408(self):
        return self.__f_2674756877849412408

    def __set_f_2674756877849412408(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_2674756877849412408 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_9151497388570990265(self):
        return self.__f_9151497388570990265

    def __set_f_9151497388570990265(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_9151497388570990265 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_1565678452235615105(self):
        return self.__f_1565678452235615105

    def __set_f_1565678452235615105(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_1565678452235615105 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_157333374141651885(self):
        return self.__f_157333374141651885

    def __set_f_157333374141651885(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_157333374141651885 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_235546436338242801(self):
        return self.__f_235546436338242801

    def __set_f_235546436338242801(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_235546436338242801 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_6462998562482886591(self):
        return self.__f_6462998562482886591

    def __set_f_6462998562482886591(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_6462998562482886591 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_8779414760933169917(self):
        return self.__f_8779414760933169917

    def __set_f_8779414760933169917(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_8779414760933169917 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_5451984308869576529(self):
        return self.__f_5451984308869576529

    def __set_f_5451984308869576529(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_5451984308869576529 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_188855504015312136(self):
        return self.__f_188855504015312136

    def __set_f_188855504015312136(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_188855504015312136 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_6368608406811834432(self):
        return self.__f_6368608406811834432

    def __set_f_6368608406811834432(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_6368608406811834432 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_8020340105449100677(self):
        return self.__f_8020340105449100677

    def __set_f_8020340105449100677(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_8020340105449100677 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_3972783259428801223(self):
        return self.__f_3972783259428801223

    def __set_f_3972783259428801223(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_3972783259428801223 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_2197059032295624775(self):
        return self.__f_2197059032295624775

    def __set_f_2197059032295624775(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_2197059032295624775 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_7060794749477844133(self):
        return self.__f_7060794749477844133

    def __set_f_7060794749477844133(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_7060794749477844133 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_2745652021697515536(self):
        return self.__f_2745652021697515536

    def __set_f_2745652021697515536(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_2745652021697515536 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_6034395913105951305(self):
        return self.__f_6034395913105951305

    def __set_f_6034395913105951305(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_6034395913105951305 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_916767987577961714(self):
        return self.__f_916767987577961714

    def __set_f_916767987577961714(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_916767987577961714 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_2966179821931253906(self):
        return self.__f_2966179821931253906

    def __set_f_2966179821931253906(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_2966179821931253906 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_9155677745115475027(self):
        return self.__f_9155677745115475027

    def __set_f_9155677745115475027(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_9155677745115475027 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_4136853236801857886(self):
        return self.__f_4136853236801857886

    def __set_f_4136853236801857886(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_4136853236801857886 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_2985938125053332294(self):
        return self.__f_2985938125053332294

    def __set_f_2985938125053332294(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_2985938125053332294 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_2164339272227203922(self):
        return self.__f_2164339272227203922

    def __set_f_2164339272227203922(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_2164339272227203922 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_114804966380045502(self):
        return self.__f_114804966380045502

    def __set_f_114804966380045502(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_114804966380045502 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_2445336287606983664(self):
        return self.__f_2445336287606983664

    def __set_f_2445336287606983664(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_2445336287606983664 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_7151644913908691297(self):
        return self.__f_7151644913908691297

    def __set_f_7151644913908691297(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_7151644913908691297 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_1604490753204815046(self):
        return self.__f_1604490753204815046

    def __set_f_1604490753204815046(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_1604490753204815046 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_3128456386189085959(self):
        return self.__f_3128456386189085959

    def __set_f_3128456386189085959(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_3128456386189085959 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_9057435281982809915(self):
        return self.__f_9057435281982809915

    def __set_f_9057435281982809915(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_9057435281982809915 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_1353983061390515983(self):
        return self.__f_1353983061390515983

    def __set_f_1353983061390515983(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_1353983061390515983 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    def __get_f_278680869427956803(self):
        return self.__f_278680869427956803

    def __set_f_278680869427956803(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTOUT)))
        self.__f_278680869427956803 = value if isinstance(
            value, MFU_MN_PORTOUT) else MFU_MN_PORTOUT(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_9058508044500194118 = property(__get_f_9058508044500194118,
                                     __set_f_9058508044500194118)
    f_268400827519036290 = property(__get_f_268400827519036290,
                                    __set_f_268400827519036290)
    f_3804720826429252246 = property(__get_f_3804720826429252246,
                                     __set_f_3804720826429252246)
    f_4094387588779856056 = property(__get_f_4094387588779856056,
                                     __set_f_4094387588779856056)
    f_3722284515940164363 = property(__get_f_3722284515940164363,
                                     __set_f_3722284515940164363)
    f_2763215685155701833 = property(__get_f_2763215685155701833,
                                     __set_f_2763215685155701833)
    f_8809170042491063265 = property(__get_f_8809170042491063265,
                                     __set_f_8809170042491063265)
    f_2674756877849412408 = property(__get_f_2674756877849412408,
                                     __set_f_2674756877849412408)
    f_9151497388570990265 = property(__get_f_9151497388570990265,
                                     __set_f_9151497388570990265)
    f_1565678452235615105 = property(__get_f_1565678452235615105,
                                     __set_f_1565678452235615105)
    f_157333374141651885 = property(__get_f_157333374141651885,
                                    __set_f_157333374141651885)
    f_235546436338242801 = property(__get_f_235546436338242801,
                                    __set_f_235546436338242801)
    f_6462998562482886591 = property(__get_f_6462998562482886591,
                                     __set_f_6462998562482886591)
    f_8779414760933169917 = property(__get_f_8779414760933169917,
                                     __set_f_8779414760933169917)
    f_5451984308869576529 = property(__get_f_5451984308869576529,
                                     __set_f_5451984308869576529)
    f_188855504015312136 = property(__get_f_188855504015312136,
                                    __set_f_188855504015312136)
    f_6368608406811834432 = property(__get_f_6368608406811834432,
                                     __set_f_6368608406811834432)
    f_8020340105449100677 = property(__get_f_8020340105449100677,
                                     __set_f_8020340105449100677)
    f_3972783259428801223 = property(__get_f_3972783259428801223,
                                     __set_f_3972783259428801223)
    f_2197059032295624775 = property(__get_f_2197059032295624775,
                                     __set_f_2197059032295624775)
    f_7060794749477844133 = property(__get_f_7060794749477844133,
                                     __set_f_7060794749477844133)
    f_2745652021697515536 = property(__get_f_2745652021697515536,
                                     __set_f_2745652021697515536)
    f_6034395913105951305 = property(__get_f_6034395913105951305,
                                     __set_f_6034395913105951305)
    f_916767987577961714 = property(__get_f_916767987577961714,
                                    __set_f_916767987577961714)
    f_2966179821931253906 = property(__get_f_2966179821931253906,
                                     __set_f_2966179821931253906)
    f_9155677745115475027 = property(__get_f_9155677745115475027,
                                     __set_f_9155677745115475027)
    f_4136853236801857886 = property(__get_f_4136853236801857886,
                                     __set_f_4136853236801857886)
    f_2985938125053332294 = property(__get_f_2985938125053332294,
                                     __set_f_2985938125053332294)
    f_2164339272227203922 = property(__get_f_2164339272227203922,
                                     __set_f_2164339272227203922)
    f_114804966380045502 = property(__get_f_114804966380045502,
                                    __set_f_114804966380045502)
    f_2445336287606983664 = property(__get_f_2445336287606983664,
                                     __set_f_2445336287606983664)
    f_7151644913908691297 = property(__get_f_7151644913908691297,
                                     __set_f_7151644913908691297)
    f_1604490753204815046 = property(__get_f_1604490753204815046,
                                     __set_f_1604490753204815046)
    f_3128456386189085959 = property(__get_f_3128456386189085959,
                                     __set_f_3128456386189085959)
    f_9057435281982809915 = property(__get_f_9057435281982809915,
                                     __set_f_9057435281982809915)
    f_1353983061390515983 = property(__get_f_1353983061390515983,
                                     __set_f_1353983061390515983)
    f_278680869427956803 = property(__get_f_278680869427956803,
                                    __set_f_278680869427956803)


class inst_i_7317298242942939054(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_3217332499044511084: [int, 2]  # type: ignore
    __f_9146625569486742957: [datatype.uint32, 32]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(6)

        self.__f_9146625569486742957 = int(0)
        cf_str += '>u32'
        self.__f_3217332499044511084 = int(0)
        cf_str += '>u2'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(136)

    def fields(
        self,
        f_3217332499044511084: int = None,
        f_9146625569486742957: int = None,
    ):
        if f_3217332499044511084:
            self.f_3217332499044511084 = f_3217332499044511084
        if f_9146625569486742957:
            self.f_9146625569486742957 = f_9146625569486742957
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_9146625569486742957),
            int(self.f_3217332499044511084),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 6
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x88
        (
            self.f_9146625569486742957,
            self.f_3217332499044511084,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_7317298242942939054(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_7317298242942939054().fields(\n'
        res += '\tf_3217332499044511084 = %s ,\n' % str(
            self.f_3217332499044511084)
        res += '\tf_9146625569486742957 = %s ,\n' % str(
            self.f_9146625569486742957)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 6

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_3217332499044511084(self):
        return self.__f_3217332499044511084

    def __set_f_3217332499044511084(self, value):
        assert int(value) < 2**2

        assert int(value) >= 0

        self.__f_3217332499044511084 = int(value)

    def __get_f_9146625569486742957(self):
        return self.__f_9146625569486742957

    def __set_f_9146625569486742957(self, value):
        assert int(value) < 2**32

        assert int(value) >= 0

        self.__f_9146625569486742957 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_3217332499044511084 = property(__get_f_3217332499044511084,
                                     __set_f_3217332499044511084)
    f_9146625569486742957 = property(__get_f_9146625569486742957,
                                     __set_f_9146625569486742957)


class inst_i_4940390838445604897(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_7566330350496992108: [datatype.uint8, 8]  # type: ignore
    __f_7818271317935764546: [STRIDE_GLB, 64]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int, STRIDE_GLB,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        self.__f_7818271317935764546 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_7566330350496992108 = int(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(137)

    def fields(
        self,
        f_7566330350496992108: int = None,
        f_7818271317935764546: STRIDE_GLB = None,
    ):
        if f_7566330350496992108:
            self.f_7566330350496992108 = f_7566330350496992108
        if f_7818271317935764546:
            self.f_7818271317935764546 = f_7818271317935764546
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_7818271317935764546),
            int(self.f_7566330350496992108),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 10
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x89
        (
            self.f_7818271317935764546,
            self.f_7566330350496992108,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_4940390838445604897(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_4940390838445604897().fields(\n'
        res += '\tf_7566330350496992108 = %s ,\n' % str(
            self.f_7566330350496992108)
        res += '\tf_7818271317935764546 = %s ,\n' % str(
            self.f_7818271317935764546)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 10

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_7566330350496992108(self):
        return self.__f_7566330350496992108

    def __set_f_7566330350496992108(self, value):
        assert int(value) < 2**8

        assert int(value) >= 0

        self.__f_7566330350496992108 = int(value)

    def __get_f_7818271317935764546(self):
        return self.__f_7818271317935764546

    def __set_f_7818271317935764546(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_7818271317935764546 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_7566330350496992108 = property(__get_f_7566330350496992108,
                                     __set_f_7566330350496992108)
    f_7818271317935764546 = property(__get_f_7818271317935764546,
                                     __set_f_7818271317935764546)


class inst_i_7071148236208088088(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_1218174442252260153: [STRIDE_GLB, 64]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[STRIDE_GLB,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        self.__f_1218174442252260153 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(138)

    def fields(
        self,
        f_1218174442252260153: STRIDE_GLB = None,
    ):
        if f_1218174442252260153:
            self.f_1218174442252260153 = f_1218174442252260153
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_1218174442252260153),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 9
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x8a
        (
            self.f_1218174442252260153,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_7071148236208088088(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_7071148236208088088().fields(\n'
        res += '\tf_1218174442252260153 = %s ,\n' % str(
            self.f_1218174442252260153)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 9

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_1218174442252260153(self):
        return self.__f_1218174442252260153

    def __set_f_1218174442252260153(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_1218174442252260153 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_1218174442252260153 = property(__get_f_1218174442252260153,
                                     __set_f_1218174442252260153)


class inst_i_3215644467781021096(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_6920772091196212887: [CCRCLR, 8]  # type: ignore
    __f_1851582658599760477: [CCRSET, 11]  # type: ignore
    __f_4535149732094779661: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_581203445514181141: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_881633176595243167: [int, 5]  # type: ignore
    __f_9201637224213811787: [int, 5]  # type: ignore
    __f_679841282522090738: [int, 5]  # type: ignore
    __f_1449988654089269400: [datatype.uint16, 16]  # type: ignore
    __f_8538332288708448876: [datatype.uint16, 16]  # type: ignore
    __f_8660001712953173509: [datatype.uint16, 16]  # type: ignore
    __f_2401380060870497267: [datatype.uint16, 16]  # type: ignore
    __f_3891171309507685859: [datatype.uint16, 16]  # type: ignore
    __f_470775771604013724: [datatype.uint16, 16]  # type: ignore
    __f_1903538310092688587: [datatype.uint8, 8]  # type: ignore
    __f_2617505763564278546: [datatype.uint8, 8]  # type: ignore
    __f_6226735239301116980: [datatype.uint8, 8]  # type: ignore
    __f_668843506724768408: [datatype.uint8, 8]  # type: ignore
    __f_6402563436718652275: [datatype.uint8, 8]  # type: ignore
    __f_7097397218627294709: [datatype.uint8, 8]  # type: ignore
    __f_592763409212270165: [datatype.uint8, 8]  # type: ignore
    __f_6323181395591066315: [MFU_PDP_OP, 2]  # type: ignore
    __f_4489512647335783385: [int, 1]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, CCRSET, ADDR_GLB_8_WITH_BANK,
                               ADDR_GLB_8_WITH_BANK, int, int, int, int, int,
                               int, int, int, int, int, int, int, int, int, int,
                               int, MFU_PDP_OP, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(1)

        self.__f_4489512647335783385 = int(0)
        cf_str += '>u1'
        self.__f_6323181395591066315 = MFU_PDP_OP(0)
        cf_str += '>u2'
        self.__f_592763409212270165 = int(0)
        cf_str += '>u8'
        self.__f_7097397218627294709 = int(0)
        cf_str += '>u8'
        self.__f_6402563436718652275 = int(0)
        cf_str += '>u8'
        self.__f_668843506724768408 = int(0)
        cf_str += '>u8'
        self.__f_6226735239301116980 = int(0)
        cf_str += '>u8'
        self.__f_2617505763564278546 = int(0)
        cf_str += '>u8'
        self.__f_1903538310092688587 = int(0)
        cf_str += '>u8'
        self.__f_470775771604013724 = int(0)
        cf_str += '>u16'
        self.__f_3891171309507685859 = int(0)
        cf_str += '>u16'
        self.__f_2401380060870497267 = int(0)
        cf_str += '>u16'
        self.__f_8660001712953173509 = int(0)
        cf_str += '>u16'
        self.__f_8538332288708448876 = int(0)
        cf_str += '>u16'
        self.__f_1449988654089269400 = int(0)
        cf_str += '>u16'
        self.__f_679841282522090738 = int(0)
        cf_str += '>u5'
        self.__f_9201637224213811787 = int(0)
        cf_str += '>u5'
        self.__f_881633176595243167 = int(0)
        cf_str += '>u5'
        self.__f_581203445514181141 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_4535149732094779661 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_1851582658599760477 = CCRSET(0)
        cf_str += '>u11'
        self.__f_6920772091196212887 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(139)

    def fields(
        self,
        f_6920772091196212887: CCRCLR = None,
        f_1851582658599760477: CCRSET = None,
        f_4535149732094779661: ADDR_GLB_8_WITH_BANK = None,
        f_581203445514181141: ADDR_GLB_8_WITH_BANK = None,
        f_881633176595243167: int = None,
        f_9201637224213811787: int = None,
        f_679841282522090738: int = None,
        f_1449988654089269400: int = None,
        f_8538332288708448876: int = None,
        f_8660001712953173509: int = None,
        f_2401380060870497267: int = None,
        f_3891171309507685859: int = None,
        f_470775771604013724: int = None,
        f_1903538310092688587: int = None,
        f_2617505763564278546: int = None,
        f_6226735239301116980: int = None,
        f_668843506724768408: int = None,
        f_6402563436718652275: int = None,
        f_7097397218627294709: int = None,
        f_592763409212270165: int = None,
        f_6323181395591066315: MFU_PDP_OP = None,
        f_4489512647335783385: int = None,
    ):
        if f_6920772091196212887:
            self.f_6920772091196212887 = f_6920772091196212887
        if f_1851582658599760477:
            self.f_1851582658599760477 = f_1851582658599760477
        if f_4535149732094779661:
            self.f_4535149732094779661 = f_4535149732094779661
        if f_581203445514181141:
            self.f_581203445514181141 = f_581203445514181141
        if f_881633176595243167:
            self.f_881633176595243167 = f_881633176595243167
        if f_9201637224213811787:
            self.f_9201637224213811787 = f_9201637224213811787
        if f_679841282522090738:
            self.f_679841282522090738 = f_679841282522090738
        if f_1449988654089269400:
            self.f_1449988654089269400 = f_1449988654089269400
        if f_8538332288708448876:
            self.f_8538332288708448876 = f_8538332288708448876
        if f_8660001712953173509:
            self.f_8660001712953173509 = f_8660001712953173509
        if f_2401380060870497267:
            self.f_2401380060870497267 = f_2401380060870497267
        if f_3891171309507685859:
            self.f_3891171309507685859 = f_3891171309507685859
        if f_470775771604013724:
            self.f_470775771604013724 = f_470775771604013724
        if f_1903538310092688587:
            self.f_1903538310092688587 = f_1903538310092688587
        if f_2617505763564278546:
            self.f_2617505763564278546 = f_2617505763564278546
        if f_6226735239301116980:
            self.f_6226735239301116980 = f_6226735239301116980
        if f_668843506724768408:
            self.f_668843506724768408 = f_668843506724768408
        if f_6402563436718652275:
            self.f_6402563436718652275 = f_6402563436718652275
        if f_7097397218627294709:
            self.f_7097397218627294709 = f_7097397218627294709
        if f_592763409212270165:
            self.f_592763409212270165 = f_592763409212270165
        if f_6323181395591066315:
            self.f_6323181395591066315 = f_6323181395591066315
        if f_4489512647335783385:
            self.f_4489512647335783385 = f_4489512647335783385
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_4489512647335783385),
            int(self.f_6323181395591066315),
            int(self.f_592763409212270165),
            int(self.f_7097397218627294709),
            int(self.f_6402563436718652275),
            int(self.f_668843506724768408),
            int(self.f_6226735239301116980),
            int(self.f_2617505763564278546),
            int(self.f_1903538310092688587),
            int(self.f_470775771604013724),
            int(self.f_3891171309507685859),
            int(self.f_2401380060870497267),
            int(self.f_8660001712953173509),
            int(self.f_8538332288708448876),
            int(self.f_1449988654089269400),
            int(self.f_679841282522090738),
            int(self.f_9201637224213811787),
            int(self.f_881633176595243167),
            int(self.f_581203445514181141),
            int(self.f_4535149732094779661),
            int(self.f_1851582658599760477),
            int(self.f_6920772091196212887),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 31
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x8b
        (
            self.f_4489512647335783385,
            self.f_6323181395591066315,
            self.f_592763409212270165,
            self.f_7097397218627294709,
            self.f_6402563436718652275,
            self.f_668843506724768408,
            self.f_6226735239301116980,
            self.f_2617505763564278546,
            self.f_1903538310092688587,
            self.f_470775771604013724,
            self.f_3891171309507685859,
            self.f_2401380060870497267,
            self.f_8660001712953173509,
            self.f_8538332288708448876,
            self.f_1449988654089269400,
            self.f_679841282522090738,
            self.f_9201637224213811787,
            self.f_881633176595243167,
            self.f_581203445514181141,
            self.f_4535149732094779661,
            self.f_1851582658599760477,
            self.f_6920772091196212887,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_3215644467781021096(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_3215644467781021096().fields(\n'
        res += '\tf_6920772091196212887 = %s ,\n' % str(
            self.f_6920772091196212887)
        res += '\tf_1851582658599760477 = %s ,\n' % str(
            self.f_1851582658599760477)
        res += '\tf_4535149732094779661 = %s ,\n' % str(
            self.f_4535149732094779661)
        res += '\tf_581203445514181141 = %s ,\n' % str(
            self.f_581203445514181141)
        res += '\tf_881633176595243167 = %s ,\n' % str(
            self.f_881633176595243167)
        res += '\tf_9201637224213811787 = %s ,\n' % str(
            self.f_9201637224213811787)
        res += '\tf_679841282522090738 = %s ,\n' % str(
            self.f_679841282522090738)
        res += '\tf_1449988654089269400 = %s ,\n' % str(
            self.f_1449988654089269400)
        res += '\tf_8538332288708448876 = %s ,\n' % str(
            self.f_8538332288708448876)
        res += '\tf_8660001712953173509 = %s ,\n' % str(
            self.f_8660001712953173509)
        res += '\tf_2401380060870497267 = %s ,\n' % str(
            self.f_2401380060870497267)
        res += '\tf_3891171309507685859 = %s ,\n' % str(
            self.f_3891171309507685859)
        res += '\tf_470775771604013724 = %s ,\n' % str(
            self.f_470775771604013724)
        res += '\tf_1903538310092688587 = %s ,\n' % str(
            self.f_1903538310092688587)
        res += '\tf_2617505763564278546 = %s ,\n' % str(
            self.f_2617505763564278546)
        res += '\tf_6226735239301116980 = %s ,\n' % str(
            self.f_6226735239301116980)
        res += '\tf_668843506724768408 = %s ,\n' % str(
            self.f_668843506724768408)
        res += '\tf_6402563436718652275 = %s ,\n' % str(
            self.f_6402563436718652275)
        res += '\tf_7097397218627294709 = %s ,\n' % str(
            self.f_7097397218627294709)
        res += '\tf_592763409212270165 = %s ,\n' % str(
            self.f_592763409212270165)
        res += '\tf_6323181395591066315 = %s ,\n' % str(
            self.f_6323181395591066315)
        res += '\tf_4489512647335783385 = %s ,\n' % str(
            self.f_4489512647335783385)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 31

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_6920772091196212887(self):
        return self.__f_6920772091196212887

    def __set_f_6920772091196212887(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_6920772091196212887 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1851582658599760477(self):
        return self.__f_1851582658599760477

    def __set_f_1851582658599760477(self, value):

        assert (isinstance(value, (int, CCRSET)))
        self.__f_1851582658599760477 = value if isinstance(
            value, CCRSET) else CCRSET(value)

    def __get_f_4535149732094779661(self):
        return self.__f_4535149732094779661

    def __set_f_4535149732094779661(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_4535149732094779661 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_581203445514181141(self):
        return self.__f_581203445514181141

    def __set_f_581203445514181141(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_581203445514181141 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_881633176595243167(self):
        return self.__f_881633176595243167

    def __set_f_881633176595243167(self, value):
        assert int(value) < 2**5

        assert int(value) >= 0

        self.__f_881633176595243167 = int(value)

    def __get_f_9201637224213811787(self):
        return self.__f_9201637224213811787

    def __set_f_9201637224213811787(self, value):
        assert int(value) < 2**5

        assert int(value) >= 0

        self.__f_9201637224213811787 = int(value)

    def __get_f_679841282522090738(self):
        return self.__f_679841282522090738

    def __set_f_679841282522090738(self, value):
        assert int(value) < 2**5

        assert int(value) >= 0

        self.__f_679841282522090738 = int(value)

    def __get_f_1449988654089269400(self):
        return self.__f_1449988654089269400

    def __set_f_1449988654089269400(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1449988654089269400 = int(value)

    def __get_f_8538332288708448876(self):
        return self.__f_8538332288708448876

    def __set_f_8538332288708448876(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8538332288708448876 = int(value)

    def __get_f_8660001712953173509(self):
        return self.__f_8660001712953173509

    def __set_f_8660001712953173509(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8660001712953173509 = int(value)

    def __get_f_2401380060870497267(self):
        return self.__f_2401380060870497267

    def __set_f_2401380060870497267(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_2401380060870497267 = int(value)

    def __get_f_3891171309507685859(self):
        return self.__f_3891171309507685859

    def __set_f_3891171309507685859(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_3891171309507685859 = int(value)

    def __get_f_470775771604013724(self):
        return self.__f_470775771604013724

    def __set_f_470775771604013724(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_470775771604013724 = int(value)

    def __get_f_1903538310092688587(self):
        return self.__f_1903538310092688587

    def __set_f_1903538310092688587(self, value):
        assert int(value) < 2**8

        assert int(value) >= 0

        self.__f_1903538310092688587 = int(value)

    def __get_f_2617505763564278546(self):
        return self.__f_2617505763564278546

    def __set_f_2617505763564278546(self, value):
        assert int(value) < 2**8

        assert int(value) >= 0

        self.__f_2617505763564278546 = int(value)

    def __get_f_6226735239301116980(self):
        return self.__f_6226735239301116980

    def __set_f_6226735239301116980(self, value):
        assert int(value) < 2**8

        assert int(value) >= 0

        self.__f_6226735239301116980 = int(value)

    def __get_f_668843506724768408(self):
        return self.__f_668843506724768408

    def __set_f_668843506724768408(self, value):
        assert int(value) < 2**8

        assert int(value) >= 0

        self.__f_668843506724768408 = int(value)

    def __get_f_6402563436718652275(self):
        return self.__f_6402563436718652275

    def __set_f_6402563436718652275(self, value):
        assert int(value) < 2**8

        assert int(value) >= 0

        self.__f_6402563436718652275 = int(value)

    def __get_f_7097397218627294709(self):
        return self.__f_7097397218627294709

    def __set_f_7097397218627294709(self, value):
        assert int(value) < 2**8

        assert int(value) >= 0

        self.__f_7097397218627294709 = int(value)

    def __get_f_592763409212270165(self):
        return self.__f_592763409212270165

    def __set_f_592763409212270165(self, value):
        assert int(value) < 2**8

        assert int(value) >= 0

        self.__f_592763409212270165 = int(value)

    def __get_f_6323181395591066315(self):
        return self.__f_6323181395591066315

    def __set_f_6323181395591066315(self, value):

        assert (isinstance(value, (int, MFU_PDP_OP)))
        self.__f_6323181395591066315 = value if isinstance(
            value, MFU_PDP_OP) else MFU_PDP_OP(value)

    def __get_f_4489512647335783385(self):
        return self.__f_4489512647335783385

    def __set_f_4489512647335783385(self, value):
        assert int(value) < 2**1

        assert int(value) >= 0

        self.__f_4489512647335783385 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_6920772091196212887 = property(__get_f_6920772091196212887,
                                     __set_f_6920772091196212887)
    f_1851582658599760477 = property(__get_f_1851582658599760477,
                                     __set_f_1851582658599760477)
    f_4535149732094779661 = property(__get_f_4535149732094779661,
                                     __set_f_4535149732094779661)
    f_581203445514181141 = property(__get_f_581203445514181141,
                                    __set_f_581203445514181141)
    f_881633176595243167 = property(__get_f_881633176595243167,
                                    __set_f_881633176595243167)
    f_9201637224213811787 = property(__get_f_9201637224213811787,
                                     __set_f_9201637224213811787)
    f_679841282522090738 = property(__get_f_679841282522090738,
                                    __set_f_679841282522090738)
    f_1449988654089269400 = property(__get_f_1449988654089269400,
                                     __set_f_1449988654089269400)
    f_8538332288708448876 = property(__get_f_8538332288708448876,
                                     __set_f_8538332288708448876)
    f_8660001712953173509 = property(__get_f_8660001712953173509,
                                     __set_f_8660001712953173509)
    f_2401380060870497267 = property(__get_f_2401380060870497267,
                                     __set_f_2401380060870497267)
    f_3891171309507685859 = property(__get_f_3891171309507685859,
                                     __set_f_3891171309507685859)
    f_470775771604013724 = property(__get_f_470775771604013724,
                                    __set_f_470775771604013724)
    f_1903538310092688587 = property(__get_f_1903538310092688587,
                                     __set_f_1903538310092688587)
    f_2617505763564278546 = property(__get_f_2617505763564278546,
                                     __set_f_2617505763564278546)
    f_6226735239301116980 = property(__get_f_6226735239301116980,
                                     __set_f_6226735239301116980)
    f_668843506724768408 = property(__get_f_668843506724768408,
                                    __set_f_668843506724768408)
    f_6402563436718652275 = property(__get_f_6402563436718652275,
                                     __set_f_6402563436718652275)
    f_7097397218627294709 = property(__get_f_7097397218627294709,
                                     __set_f_7097397218627294709)
    f_592763409212270165 = property(__get_f_592763409212270165,
                                    __set_f_592763409212270165)
    f_6323181395591066315 = property(__get_f_6323181395591066315,
                                     __set_f_6323181395591066315)
    f_4489512647335783385 = property(__get_f_4489512647335783385,
                                     __set_f_4489512647335783385)


class inst_i_4300588898699658039(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_8931313174680033219: [datatype.uint16, 16]  # type: ignore
    __f_3028220947580239299: [datatype.uint16, 16]  # type: ignore
    __f_7919268989332022720: [datatype.uint16, 16]  # type: ignore
    __f_1203634781404531294: [datatype.uint16, 16]  # type: ignore
    __f_8166952301032877815: [datatype.uint16, 16]  # type: ignore
    __f_1439106843142557891: [datatype.uint16, 16]  # type: ignore
    __f_8311800582383395327: [STRIDE_GLB, 64]  # type: ignore
    __f_993290916930932757: [datatype.uint16, 16]  # type: ignore
    __f_1729609380278631659: [datatype.uint16, 16]  # type: ignore
    __f_7570108842447095558: [datatype.uint16, 16]  # type: ignore
    __f_4003207286705832500: [datatype.uint16, 16]  # type: ignore
    __f_4875701691136722882: [STRIDE_GLB, 64]  # type: ignore
    __f_7308482092233284198: [datatype.uint16, 16]  # type: ignore
    __f_2755877793672541565: [datatype.uint16, 16]  # type: ignore
    __f_6493016072301960846: [datatype.uint16, 16]  # type: ignore
    __f_7382350298538785663: [datatype.uint16, 16]  # type: ignore
    __f_1096163640311303935: [datatype.uint16, 16]  # type: ignore
    __f_3161247888941852461: [datatype.uint16, 16]  # type: ignore
    __f_6686934391189217649: [datatype.uint16, 16]  # type: ignore
    __f_7413516581902498076: [datatype.uint16, 16]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[int, int, int, int, int, int, STRIDE_GLB, int,
                               int, int, int, STRIDE_GLB, int, int, int, int,
                               int, int, int, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        self.__f_7413516581902498076 = int(0)
        cf_str += '>u16'
        self.__f_6686934391189217649 = int(0)
        cf_str += '>u16'
        self.__f_3161247888941852461 = int(0)
        cf_str += '>u16'
        self.__f_1096163640311303935 = int(0)
        cf_str += '>u16'
        self.__f_7382350298538785663 = int(0)
        cf_str += '>u16'
        self.__f_6493016072301960846 = int(0)
        cf_str += '>u16'
        self.__f_2755877793672541565 = int(0)
        cf_str += '>u16'
        self.__f_7308482092233284198 = int(0)
        cf_str += '>u16'
        self.__f_4875701691136722882 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_4003207286705832500 = int(0)
        cf_str += '>u16'
        self.__f_7570108842447095558 = int(0)
        cf_str += '>u16'
        self.__f_1729609380278631659 = int(0)
        cf_str += '>u16'
        self.__f_993290916930932757 = int(0)
        cf_str += '>u16'
        self.__f_8311800582383395327 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_1439106843142557891 = int(0)
        cf_str += '>u16'
        self.__f_8166952301032877815 = int(0)
        cf_str += '>u16'
        self.__f_1203634781404531294 = int(0)
        cf_str += '>u16'
        self.__f_7919268989332022720 = int(0)
        cf_str += '>u16'
        self.__f_3028220947580239299 = int(0)
        cf_str += '>u16'
        self.__f_8931313174680033219 = int(0)
        cf_str += '>u16'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(140)

    def fields(
        self,
        f_8931313174680033219: int = None,
        f_3028220947580239299: int = None,
        f_7919268989332022720: int = None,
        f_1203634781404531294: int = None,
        f_8166952301032877815: int = None,
        f_1439106843142557891: int = None,
        f_8311800582383395327: STRIDE_GLB = None,
        f_993290916930932757: int = None,
        f_1729609380278631659: int = None,
        f_7570108842447095558: int = None,
        f_4003207286705832500: int = None,
        f_4875701691136722882: STRIDE_GLB = None,
        f_7308482092233284198: int = None,
        f_2755877793672541565: int = None,
        f_6493016072301960846: int = None,
        f_7382350298538785663: int = None,
        f_1096163640311303935: int = None,
        f_3161247888941852461: int = None,
        f_6686934391189217649: int = None,
        f_7413516581902498076: int = None,
    ):
        if f_8931313174680033219:
            self.f_8931313174680033219 = f_8931313174680033219
        if f_3028220947580239299:
            self.f_3028220947580239299 = f_3028220947580239299
        if f_7919268989332022720:
            self.f_7919268989332022720 = f_7919268989332022720
        if f_1203634781404531294:
            self.f_1203634781404531294 = f_1203634781404531294
        if f_8166952301032877815:
            self.f_8166952301032877815 = f_8166952301032877815
        if f_1439106843142557891:
            self.f_1439106843142557891 = f_1439106843142557891
        if f_8311800582383395327:
            self.f_8311800582383395327 = f_8311800582383395327
        if f_993290916930932757:
            self.f_993290916930932757 = f_993290916930932757
        if f_1729609380278631659:
            self.f_1729609380278631659 = f_1729609380278631659
        if f_7570108842447095558:
            self.f_7570108842447095558 = f_7570108842447095558
        if f_4003207286705832500:
            self.f_4003207286705832500 = f_4003207286705832500
        if f_4875701691136722882:
            self.f_4875701691136722882 = f_4875701691136722882
        if f_7308482092233284198:
            self.f_7308482092233284198 = f_7308482092233284198
        if f_2755877793672541565:
            self.f_2755877793672541565 = f_2755877793672541565
        if f_6493016072301960846:
            self.f_6493016072301960846 = f_6493016072301960846
        if f_7382350298538785663:
            self.f_7382350298538785663 = f_7382350298538785663
        if f_1096163640311303935:
            self.f_1096163640311303935 = f_1096163640311303935
        if f_3161247888941852461:
            self.f_3161247888941852461 = f_3161247888941852461
        if f_6686934391189217649:
            self.f_6686934391189217649 = f_6686934391189217649
        if f_7413516581902498076:
            self.f_7413516581902498076 = f_7413516581902498076
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_7413516581902498076),
            int(self.f_6686934391189217649),
            int(self.f_3161247888941852461),
            int(self.f_1096163640311303935),
            int(self.f_7382350298538785663),
            int(self.f_6493016072301960846),
            int(self.f_2755877793672541565),
            int(self.f_7308482092233284198),
            int(self.f_4875701691136722882),
            int(self.f_4003207286705832500),
            int(self.f_7570108842447095558),
            int(self.f_1729609380278631659),
            int(self.f_993290916930932757),
            int(self.f_8311800582383395327),
            int(self.f_1439106843142557891),
            int(self.f_8166952301032877815),
            int(self.f_1203634781404531294),
            int(self.f_7919268989332022720),
            int(self.f_3028220947580239299),
            int(self.f_8931313174680033219),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 53
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x8c
        (
            self.f_7413516581902498076,
            self.f_6686934391189217649,
            self.f_3161247888941852461,
            self.f_1096163640311303935,
            self.f_7382350298538785663,
            self.f_6493016072301960846,
            self.f_2755877793672541565,
            self.f_7308482092233284198,
            self.f_4875701691136722882,
            self.f_4003207286705832500,
            self.f_7570108842447095558,
            self.f_1729609380278631659,
            self.f_993290916930932757,
            self.f_8311800582383395327,
            self.f_1439106843142557891,
            self.f_8166952301032877815,
            self.f_1203634781404531294,
            self.f_7919268989332022720,
            self.f_3028220947580239299,
            self.f_8931313174680033219,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_4300588898699658039(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_4300588898699658039().fields(\n'
        res += '\tf_8931313174680033219 = %s ,\n' % str(
            self.f_8931313174680033219)
        res += '\tf_3028220947580239299 = %s ,\n' % str(
            self.f_3028220947580239299)
        res += '\tf_7919268989332022720 = %s ,\n' % str(
            self.f_7919268989332022720)
        res += '\tf_1203634781404531294 = %s ,\n' % str(
            self.f_1203634781404531294)
        res += '\tf_8166952301032877815 = %s ,\n' % str(
            self.f_8166952301032877815)
        res += '\tf_1439106843142557891 = %s ,\n' % str(
            self.f_1439106843142557891)
        res += '\tf_8311800582383395327 = %s ,\n' % str(
            self.f_8311800582383395327)
        res += '\tf_993290916930932757 = %s ,\n' % str(
            self.f_993290916930932757)
        res += '\tf_1729609380278631659 = %s ,\n' % str(
            self.f_1729609380278631659)
        res += '\tf_7570108842447095558 = %s ,\n' % str(
            self.f_7570108842447095558)
        res += '\tf_4003207286705832500 = %s ,\n' % str(
            self.f_4003207286705832500)
        res += '\tf_4875701691136722882 = %s ,\n' % str(
            self.f_4875701691136722882)
        res += '\tf_7308482092233284198 = %s ,\n' % str(
            self.f_7308482092233284198)
        res += '\tf_2755877793672541565 = %s ,\n' % str(
            self.f_2755877793672541565)
        res += '\tf_6493016072301960846 = %s ,\n' % str(
            self.f_6493016072301960846)
        res += '\tf_7382350298538785663 = %s ,\n' % str(
            self.f_7382350298538785663)
        res += '\tf_1096163640311303935 = %s ,\n' % str(
            self.f_1096163640311303935)
        res += '\tf_3161247888941852461 = %s ,\n' % str(
            self.f_3161247888941852461)
        res += '\tf_6686934391189217649 = %s ,\n' % str(
            self.f_6686934391189217649)
        res += '\tf_7413516581902498076 = %s ,\n' % str(
            self.f_7413516581902498076)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 53

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_8931313174680033219(self):
        return self.__f_8931313174680033219

    def __set_f_8931313174680033219(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8931313174680033219 = int(value)

    def __get_f_3028220947580239299(self):
        return self.__f_3028220947580239299

    def __set_f_3028220947580239299(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_3028220947580239299 = int(value)

    def __get_f_7919268989332022720(self):
        return self.__f_7919268989332022720

    def __set_f_7919268989332022720(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_7919268989332022720 = int(value)

    def __get_f_1203634781404531294(self):
        return self.__f_1203634781404531294

    def __set_f_1203634781404531294(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1203634781404531294 = int(value)

    def __get_f_8166952301032877815(self):
        return self.__f_8166952301032877815

    def __set_f_8166952301032877815(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8166952301032877815 = int(value)

    def __get_f_1439106843142557891(self):
        return self.__f_1439106843142557891

    def __set_f_1439106843142557891(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1439106843142557891 = int(value)

    def __get_f_8311800582383395327(self):
        return self.__f_8311800582383395327

    def __set_f_8311800582383395327(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_8311800582383395327 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_993290916930932757(self):
        return self.__f_993290916930932757

    def __set_f_993290916930932757(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_993290916930932757 = int(value)

    def __get_f_1729609380278631659(self):
        return self.__f_1729609380278631659

    def __set_f_1729609380278631659(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1729609380278631659 = int(value)

    def __get_f_7570108842447095558(self):
        return self.__f_7570108842447095558

    def __set_f_7570108842447095558(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_7570108842447095558 = int(value)

    def __get_f_4003207286705832500(self):
        return self.__f_4003207286705832500

    def __set_f_4003207286705832500(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_4003207286705832500 = int(value)

    def __get_f_4875701691136722882(self):
        return self.__f_4875701691136722882

    def __set_f_4875701691136722882(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_4875701691136722882 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_7308482092233284198(self):
        return self.__f_7308482092233284198

    def __set_f_7308482092233284198(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_7308482092233284198 = int(value)

    def __get_f_2755877793672541565(self):
        return self.__f_2755877793672541565

    def __set_f_2755877793672541565(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_2755877793672541565 = int(value)

    def __get_f_6493016072301960846(self):
        return self.__f_6493016072301960846

    def __set_f_6493016072301960846(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_6493016072301960846 = int(value)

    def __get_f_7382350298538785663(self):
        return self.__f_7382350298538785663

    def __set_f_7382350298538785663(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_7382350298538785663 = int(value)

    def __get_f_1096163640311303935(self):
        return self.__f_1096163640311303935

    def __set_f_1096163640311303935(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1096163640311303935 = int(value)

    def __get_f_3161247888941852461(self):
        return self.__f_3161247888941852461

    def __set_f_3161247888941852461(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_3161247888941852461 = int(value)

    def __get_f_6686934391189217649(self):
        return self.__f_6686934391189217649

    def __set_f_6686934391189217649(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_6686934391189217649 = int(value)

    def __get_f_7413516581902498076(self):
        return self.__f_7413516581902498076

    def __set_f_7413516581902498076(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_7413516581902498076 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_8931313174680033219 = property(__get_f_8931313174680033219,
                                     __set_f_8931313174680033219)
    f_3028220947580239299 = property(__get_f_3028220947580239299,
                                     __set_f_3028220947580239299)
    f_7919268989332022720 = property(__get_f_7919268989332022720,
                                     __set_f_7919268989332022720)
    f_1203634781404531294 = property(__get_f_1203634781404531294,
                                     __set_f_1203634781404531294)
    f_8166952301032877815 = property(__get_f_8166952301032877815,
                                     __set_f_8166952301032877815)
    f_1439106843142557891 = property(__get_f_1439106843142557891,
                                     __set_f_1439106843142557891)
    f_8311800582383395327 = property(__get_f_8311800582383395327,
                                     __set_f_8311800582383395327)
    f_993290916930932757 = property(__get_f_993290916930932757,
                                    __set_f_993290916930932757)
    f_1729609380278631659 = property(__get_f_1729609380278631659,
                                     __set_f_1729609380278631659)
    f_7570108842447095558 = property(__get_f_7570108842447095558,
                                     __set_f_7570108842447095558)
    f_4003207286705832500 = property(__get_f_4003207286705832500,
                                     __set_f_4003207286705832500)
    f_4875701691136722882 = property(__get_f_4875701691136722882,
                                     __set_f_4875701691136722882)
    f_7308482092233284198 = property(__get_f_7308482092233284198,
                                     __set_f_7308482092233284198)
    f_2755877793672541565 = property(__get_f_2755877793672541565,
                                     __set_f_2755877793672541565)
    f_6493016072301960846 = property(__get_f_6493016072301960846,
                                     __set_f_6493016072301960846)
    f_7382350298538785663 = property(__get_f_7382350298538785663,
                                     __set_f_7382350298538785663)
    f_1096163640311303935 = property(__get_f_1096163640311303935,
                                     __set_f_1096163640311303935)
    f_3161247888941852461 = property(__get_f_3161247888941852461,
                                     __set_f_3161247888941852461)
    f_6686934391189217649 = property(__get_f_6686934391189217649,
                                     __set_f_6686934391189217649)
    f_7413516581902498076 = property(__get_f_7413516581902498076,
                                     __set_f_7413516581902498076)


class inst_i_4573608092199809765(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_6920772091196212887: [CCRCLR, 8]  # type: ignore
    __f_1851582658599760477: [CCRSET, 11]  # type: ignore
    __f_4535149732094779661: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_581203445514181141: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_3874332781368398897: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_1963381605522139425: [datatype.uint16, 16]  # type: ignore
    __f_4747793698969443428: [datatype.uint16, 16]  # type: ignore
    __f_241270096424587545: [datatype.uint16, 16]  # type: ignore
    __f_7119465869533878975: [datatype.uint16, 16]  # type: ignore
    __f_7567046777643367421: [STRIDE_GLB, 64]  # type: ignore
    __f_7818271317935764546: [STRIDE_GLB, 64]  # type: ignore
    __f_5154053810891412609: [datatype.uint16, 16]  # type: ignore
    __f_325614278010692567: [datatype.uint16, 16]  # type: ignore
    __f_496025576879528957: [datatype.uint16, 16]  # type: ignore
    __f_1774600841097367506: [BF24, 24]  # type: ignore
    __f_7053440206010891761: [BF24, 24]  # type: ignore
    __f_1556128250887951101: [MFU_CROP_ALIGN, 2]  # type: ignore
    __f_2047135823565033355: [MFU_CROP_RESIZE, 1]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, CCRSET, ADDR_GLB_8_WITH_BANK,
                               ADDR_GLB_8_WITH_BANK, ADDR_GLB_8_WITH_BANK, int,
                               int, int, int, STRIDE_GLB, STRIDE_GLB, int, int,
                               int, BF24, BF24, MFU_CROP_ALIGN,
                               MFU_CROP_RESIZE,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(7)

        self.__f_2047135823565033355 = MFU_CROP_RESIZE(0)
        cf_str += '>u1'
        self.__f_1556128250887951101 = MFU_CROP_ALIGN(0)
        cf_str += '>u2'
        self.__f_7053440206010891761 = BF24(0)
        cf_str += '>u24'
        self.__f_1774600841097367506 = BF24(0)
        cf_str += '>u24'
        self.__f_496025576879528957 = int(0)
        cf_str += '>u16'
        self.__f_325614278010692567 = int(0)
        cf_str += '>u16'
        self.__f_5154053810891412609 = int(0)
        cf_str += '>u16'
        self.__f_7818271317935764546 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_7567046777643367421 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_7119465869533878975 = int(0)
        cf_str += '>u16'
        self.__f_241270096424587545 = int(0)
        cf_str += '>u16'
        self.__f_4747793698969443428 = int(0)
        cf_str += '>u16'
        self.__f_1963381605522139425 = int(0)
        cf_str += '>u16'
        self.__f_3874332781368398897 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_581203445514181141 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_4535149732094779661 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_1851582658599760477 = CCRSET(0)
        cf_str += '>u11'
        self.__f_6920772091196212887 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(141)

    def fields(
        self,
        f_6920772091196212887: CCRCLR = None,
        f_1851582658599760477: CCRSET = None,
        f_4535149732094779661: ADDR_GLB_8_WITH_BANK = None,
        f_581203445514181141: ADDR_GLB_8_WITH_BANK = None,
        f_3874332781368398897: ADDR_GLB_8_WITH_BANK = None,
        f_1963381605522139425: int = None,
        f_4747793698969443428: int = None,
        f_241270096424587545: int = None,
        f_7119465869533878975: int = None,
        f_7567046777643367421: STRIDE_GLB = None,
        f_7818271317935764546: STRIDE_GLB = None,
        f_5154053810891412609: int = None,
        f_325614278010692567: int = None,
        f_496025576879528957: int = None,
        f_1774600841097367506: BF24 = None,
        f_7053440206010891761: BF24 = None,
        f_1556128250887951101: MFU_CROP_ALIGN = None,
        f_2047135823565033355: MFU_CROP_RESIZE = None,
    ):
        if f_6920772091196212887:
            self.f_6920772091196212887 = f_6920772091196212887
        if f_1851582658599760477:
            self.f_1851582658599760477 = f_1851582658599760477
        if f_4535149732094779661:
            self.f_4535149732094779661 = f_4535149732094779661
        if f_581203445514181141:
            self.f_581203445514181141 = f_581203445514181141
        if f_3874332781368398897:
            self.f_3874332781368398897 = f_3874332781368398897
        if f_1963381605522139425:
            self.f_1963381605522139425 = f_1963381605522139425
        if f_4747793698969443428:
            self.f_4747793698969443428 = f_4747793698969443428
        if f_241270096424587545:
            self.f_241270096424587545 = f_241270096424587545
        if f_7119465869533878975:
            self.f_7119465869533878975 = f_7119465869533878975
        if f_7567046777643367421:
            self.f_7567046777643367421 = f_7567046777643367421
        if f_7818271317935764546:
            self.f_7818271317935764546 = f_7818271317935764546
        if f_5154053810891412609:
            self.f_5154053810891412609 = f_5154053810891412609
        if f_325614278010692567:
            self.f_325614278010692567 = f_325614278010692567
        if f_496025576879528957:
            self.f_496025576879528957 = f_496025576879528957
        if f_1774600841097367506:
            self.f_1774600841097367506 = f_1774600841097367506
        if f_7053440206010891761:
            self.f_7053440206010891761 = f_7053440206010891761
        if f_1556128250887951101:
            self.f_1556128250887951101 = f_1556128250887951101
        if f_2047135823565033355:
            self.f_2047135823565033355 = f_2047135823565033355
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_2047135823565033355),
            int(self.f_1556128250887951101),
            int(self.f_7053440206010891761),
            int(self.f_1774600841097367506),
            int(self.f_496025576879528957),
            int(self.f_325614278010692567),
            int(self.f_5154053810891412609),
            int(self.f_7818271317935764546),
            int(self.f_7567046777643367421),
            int(self.f_7119465869533878975),
            int(self.f_241270096424587545),
            int(self.f_4747793698969443428),
            int(self.f_1963381605522139425),
            int(self.f_3874332781368398897),
            int(self.f_581203445514181141),
            int(self.f_4535149732094779661),
            int(self.f_1851582658599760477),
            int(self.f_6920772091196212887),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 50
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x8d
        (
            self.f_2047135823565033355,
            self.f_1556128250887951101,
            self.f_7053440206010891761,
            self.f_1774600841097367506,
            self.f_496025576879528957,
            self.f_325614278010692567,
            self.f_5154053810891412609,
            self.f_7818271317935764546,
            self.f_7567046777643367421,
            self.f_7119465869533878975,
            self.f_241270096424587545,
            self.f_4747793698969443428,
            self.f_1963381605522139425,
            self.f_3874332781368398897,
            self.f_581203445514181141,
            self.f_4535149732094779661,
            self.f_1851582658599760477,
            self.f_6920772091196212887,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_4573608092199809765(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_4573608092199809765().fields(\n'
        res += '\tf_6920772091196212887 = %s ,\n' % str(
            self.f_6920772091196212887)
        res += '\tf_1851582658599760477 = %s ,\n' % str(
            self.f_1851582658599760477)
        res += '\tf_4535149732094779661 = %s ,\n' % str(
            self.f_4535149732094779661)
        res += '\tf_581203445514181141 = %s ,\n' % str(
            self.f_581203445514181141)
        res += '\tf_3874332781368398897 = %s ,\n' % str(
            self.f_3874332781368398897)
        res += '\tf_1963381605522139425 = %s ,\n' % str(
            self.f_1963381605522139425)
        res += '\tf_4747793698969443428 = %s ,\n' % str(
            self.f_4747793698969443428)
        res += '\tf_241270096424587545 = %s ,\n' % str(
            self.f_241270096424587545)
        res += '\tf_7119465869533878975 = %s ,\n' % str(
            self.f_7119465869533878975)
        res += '\tf_7567046777643367421 = %s ,\n' % str(
            self.f_7567046777643367421)
        res += '\tf_7818271317935764546 = %s ,\n' % str(
            self.f_7818271317935764546)
        res += '\tf_5154053810891412609 = %s ,\n' % str(
            self.f_5154053810891412609)
        res += '\tf_325614278010692567 = %s ,\n' % str(
            self.f_325614278010692567)
        res += '\tf_496025576879528957 = %s ,\n' % str(
            self.f_496025576879528957)
        res += '\tf_1774600841097367506 = %s ,\n' % str(
            self.f_1774600841097367506)
        res += '\tf_7053440206010891761 = %s ,\n' % str(
            self.f_7053440206010891761)
        res += '\tf_1556128250887951101 = %s ,\n' % str(
            self.f_1556128250887951101)
        res += '\tf_2047135823565033355 = %s ,\n' % str(
            self.f_2047135823565033355)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 50

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_6920772091196212887(self):
        return self.__f_6920772091196212887

    def __set_f_6920772091196212887(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_6920772091196212887 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1851582658599760477(self):
        return self.__f_1851582658599760477

    def __set_f_1851582658599760477(self, value):

        assert (isinstance(value, (int, CCRSET)))
        self.__f_1851582658599760477 = value if isinstance(
            value, CCRSET) else CCRSET(value)

    def __get_f_4535149732094779661(self):
        return self.__f_4535149732094779661

    def __set_f_4535149732094779661(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_4535149732094779661 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_581203445514181141(self):
        return self.__f_581203445514181141

    def __set_f_581203445514181141(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_581203445514181141 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_3874332781368398897(self):
        return self.__f_3874332781368398897

    def __set_f_3874332781368398897(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_3874332781368398897 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_1963381605522139425(self):
        return self.__f_1963381605522139425

    def __set_f_1963381605522139425(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1963381605522139425 = int(value)

    def __get_f_4747793698969443428(self):
        return self.__f_4747793698969443428

    def __set_f_4747793698969443428(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_4747793698969443428 = int(value)

    def __get_f_241270096424587545(self):
        return self.__f_241270096424587545

    def __set_f_241270096424587545(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_241270096424587545 = int(value)

    def __get_f_7119465869533878975(self):
        return self.__f_7119465869533878975

    def __set_f_7119465869533878975(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_7119465869533878975 = int(value)

    def __get_f_7567046777643367421(self):
        return self.__f_7567046777643367421

    def __set_f_7567046777643367421(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_7567046777643367421 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_7818271317935764546(self):
        return self.__f_7818271317935764546

    def __set_f_7818271317935764546(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_7818271317935764546 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_5154053810891412609(self):
        return self.__f_5154053810891412609

    def __set_f_5154053810891412609(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_5154053810891412609 = int(value)

    def __get_f_325614278010692567(self):
        return self.__f_325614278010692567

    def __set_f_325614278010692567(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_325614278010692567 = int(value)

    def __get_f_496025576879528957(self):
        return self.__f_496025576879528957

    def __set_f_496025576879528957(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_496025576879528957 = int(value)

    def __get_f_1774600841097367506(self):
        return self.__f_1774600841097367506

    def __set_f_1774600841097367506(self, value):

        assert (isinstance(value, (int, BF24)))
        self.__f_1774600841097367506 = value if isinstance(
            value, BF24) else BF24(value)

    def __get_f_7053440206010891761(self):
        return self.__f_7053440206010891761

    def __set_f_7053440206010891761(self, value):

        assert (isinstance(value, (int, BF24)))
        self.__f_7053440206010891761 = value if isinstance(
            value, BF24) else BF24(value)

    def __get_f_1556128250887951101(self):
        return self.__f_1556128250887951101

    def __set_f_1556128250887951101(self, value):

        assert (isinstance(value, (int, MFU_CROP_ALIGN)))
        self.__f_1556128250887951101 = value if isinstance(
            value, MFU_CROP_ALIGN) else MFU_CROP_ALIGN(value)

    def __get_f_2047135823565033355(self):
        return self.__f_2047135823565033355

    def __set_f_2047135823565033355(self, value):

        assert (isinstance(value, (int, MFU_CROP_RESIZE)))
        self.__f_2047135823565033355 = value if isinstance(
            value, MFU_CROP_RESIZE) else MFU_CROP_RESIZE(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_6920772091196212887 = property(__get_f_6920772091196212887,
                                     __set_f_6920772091196212887)
    f_1851582658599760477 = property(__get_f_1851582658599760477,
                                     __set_f_1851582658599760477)
    f_4535149732094779661 = property(__get_f_4535149732094779661,
                                     __set_f_4535149732094779661)
    f_581203445514181141 = property(__get_f_581203445514181141,
                                    __set_f_581203445514181141)
    f_3874332781368398897 = property(__get_f_3874332781368398897,
                                     __set_f_3874332781368398897)
    f_1963381605522139425 = property(__get_f_1963381605522139425,
                                     __set_f_1963381605522139425)
    f_4747793698969443428 = property(__get_f_4747793698969443428,
                                     __set_f_4747793698969443428)
    f_241270096424587545 = property(__get_f_241270096424587545,
                                    __set_f_241270096424587545)
    f_7119465869533878975 = property(__get_f_7119465869533878975,
                                     __set_f_7119465869533878975)
    f_7567046777643367421 = property(__get_f_7567046777643367421,
                                     __set_f_7567046777643367421)
    f_7818271317935764546 = property(__get_f_7818271317935764546,
                                     __set_f_7818271317935764546)
    f_5154053810891412609 = property(__get_f_5154053810891412609,
                                     __set_f_5154053810891412609)
    f_325614278010692567 = property(__get_f_325614278010692567,
                                    __set_f_325614278010692567)
    f_496025576879528957 = property(__get_f_496025576879528957,
                                    __set_f_496025576879528957)
    f_1774600841097367506 = property(__get_f_1774600841097367506,
                                     __set_f_1774600841097367506)
    f_7053440206010891761 = property(__get_f_7053440206010891761,
                                     __set_f_7053440206010891761)
    f_1556128250887951101 = property(__get_f_1556128250887951101,
                                     __set_f_1556128250887951101)
    f_2047135823565033355 = property(__get_f_2047135823565033355,
                                     __set_f_2047135823565033355)


class inst_i_3562245241250454416(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_1851582658599760477: [CCRSET, 11]  # type: ignore
    __f_581203445514181141: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_7714181516199238740: [datatype.uint16, 16]  # type: ignore
    __f_6102948258158759554: [int, 20]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRSET, ADDR_GLB_8_WITH_BANK, int, int,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        self.__f_6102948258158759554 = int(0)
        cf_str += '>u20'
        self.__f_7714181516199238740 = int(0)
        cf_str += '>u16'
        self.__f_581203445514181141 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_1851582658599760477 = CCRSET(0)
        cf_str += '>u11'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(142)

    def fields(
        self,
        f_1851582658599760477: CCRSET = None,
        f_581203445514181141: ADDR_GLB_8_WITH_BANK = None,
        f_7714181516199238740: int = None,
        f_6102948258158759554: int = None,
    ):
        if f_1851582658599760477:
            self.f_1851582658599760477 = f_1851582658599760477
        if f_581203445514181141:
            self.f_581203445514181141 = f_581203445514181141
        if f_7714181516199238740:
            self.f_7714181516199238740 = f_7714181516199238740
        if f_6102948258158759554:
            self.f_6102948258158759554 = f_6102948258158759554
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_6102948258158759554),
            int(self.f_7714181516199238740),
            int(self.f_581203445514181141),
            int(self.f_1851582658599760477),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 10
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x8e
        (
            self.f_6102948258158759554,
            self.f_7714181516199238740,
            self.f_581203445514181141,
            self.f_1851582658599760477,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_3562245241250454416(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_3562245241250454416().fields(\n'
        res += '\tf_1851582658599760477 = %s ,\n' % str(
            self.f_1851582658599760477)
        res += '\tf_581203445514181141 = %s ,\n' % str(
            self.f_581203445514181141)
        res += '\tf_7714181516199238740 = %s ,\n' % str(
            self.f_7714181516199238740)
        res += '\tf_6102948258158759554 = %s ,\n' % str(
            self.f_6102948258158759554)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 10

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_1851582658599760477(self):
        return self.__f_1851582658599760477

    def __set_f_1851582658599760477(self, value):

        assert (isinstance(value, (int, CCRSET)))
        self.__f_1851582658599760477 = value if isinstance(
            value, CCRSET) else CCRSET(value)

    def __get_f_581203445514181141(self):
        return self.__f_581203445514181141

    def __set_f_581203445514181141(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_581203445514181141 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_7714181516199238740(self):
        return self.__f_7714181516199238740

    def __set_f_7714181516199238740(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_7714181516199238740 = int(value)

    def __get_f_6102948258158759554(self):
        return self.__f_6102948258158759554

    def __set_f_6102948258158759554(self, value):
        assert int(value) < 2**20

        assert int(value) >= 0

        self.__f_6102948258158759554 = int(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_1851582658599760477 = property(__get_f_1851582658599760477,
                                     __set_f_1851582658599760477)
    f_581203445514181141 = property(__get_f_581203445514181141,
                                    __set_f_581203445514181141)
    f_7714181516199238740 = property(__get_f_7714181516199238740,
                                     __set_f_7714181516199238740)
    f_6102948258158759554 = property(__get_f_6102948258158759554,
                                     __set_f_6102948258158759554)


class inst_i_7361852897854452313(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_6920772091196212887: [CCRCLR, 8]  # type: ignore
    __f_1851582658599760477: [CCRSET, 11]  # type: ignore
    __f_4535149732094779661: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_581203445514181141: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_7567046777643367421: [STRIDE_GLB, 64]  # type: ignore
    __f_7818271317935764546: [STRIDE_GLB, 64]  # type: ignore
    __f_1449988654089269400: [datatype.uint16, 16]  # type: ignore
    __f_8538332288708448876: [datatype.uint16, 16]  # type: ignore
    __f_8660001712953173509: [datatype.uint16, 16]  # type: ignore
    __f_2401380060870497267: [datatype.uint16, 16]  # type: ignore
    __f_3913792219024292053: [PRECISION, 2]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, CCRSET, ADDR_GLB_8_WITH_BANK,
                               ADDR_GLB_8_WITH_BANK, STRIDE_GLB, STRIDE_GLB,
                               int, int, int, int, PRECISION,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(1)

        self.__f_3913792219024292053 = PRECISION(0)
        cf_str += '>u2'
        self.__f_2401380060870497267 = int(0)
        cf_str += '>u16'
        self.__f_8660001712953173509 = int(0)
        cf_str += '>u16'
        self.__f_8538332288708448876 = int(0)
        cf_str += '>u16'
        self.__f_1449988654089269400 = int(0)
        cf_str += '>u16'
        self.__f_7818271317935764546 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_7567046777643367421 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_581203445514181141 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_4535149732094779661 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_1851582658599760477 = CCRSET(0)
        cf_str += '>u11'
        self.__f_6920772091196212887 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(143)

    def fields(
        self,
        f_6920772091196212887: CCRCLR = None,
        f_1851582658599760477: CCRSET = None,
        f_4535149732094779661: ADDR_GLB_8_WITH_BANK = None,
        f_581203445514181141: ADDR_GLB_8_WITH_BANK = None,
        f_7567046777643367421: STRIDE_GLB = None,
        f_7818271317935764546: STRIDE_GLB = None,
        f_1449988654089269400: int = None,
        f_8538332288708448876: int = None,
        f_8660001712953173509: int = None,
        f_2401380060870497267: int = None,
        f_3913792219024292053: PRECISION = None,
    ):
        if f_6920772091196212887:
            self.f_6920772091196212887 = f_6920772091196212887
        if f_1851582658599760477:
            self.f_1851582658599760477 = f_1851582658599760477
        if f_4535149732094779661:
            self.f_4535149732094779661 = f_4535149732094779661
        if f_581203445514181141:
            self.f_581203445514181141 = f_581203445514181141
        if f_7567046777643367421:
            self.f_7567046777643367421 = f_7567046777643367421
        if f_7818271317935764546:
            self.f_7818271317935764546 = f_7818271317935764546
        if f_1449988654089269400:
            self.f_1449988654089269400 = f_1449988654089269400
        if f_8538332288708448876:
            self.f_8538332288708448876 = f_8538332288708448876
        if f_8660001712953173509:
            self.f_8660001712953173509 = f_8660001712953173509
        if f_2401380060870497267:
            self.f_2401380060870497267 = f_2401380060870497267
        if f_3913792219024292053:
            self.f_3913792219024292053 = f_3913792219024292053
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_3913792219024292053),
            int(self.f_2401380060870497267),
            int(self.f_8660001712953173509),
            int(self.f_8538332288708448876),
            int(self.f_1449988654089269400),
            int(self.f_7818271317935764546),
            int(self.f_7567046777643367421),
            int(self.f_581203445514181141),
            int(self.f_4535149732094779661),
            int(self.f_1851582658599760477),
            int(self.f_6920772091196212887),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 34
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x8f
        (
            self.f_3913792219024292053,
            self.f_2401380060870497267,
            self.f_8660001712953173509,
            self.f_8538332288708448876,
            self.f_1449988654089269400,
            self.f_7818271317935764546,
            self.f_7567046777643367421,
            self.f_581203445514181141,
            self.f_4535149732094779661,
            self.f_1851582658599760477,
            self.f_6920772091196212887,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_7361852897854452313(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_7361852897854452313().fields(\n'
        res += '\tf_6920772091196212887 = %s ,\n' % str(
            self.f_6920772091196212887)
        res += '\tf_1851582658599760477 = %s ,\n' % str(
            self.f_1851582658599760477)
        res += '\tf_4535149732094779661 = %s ,\n' % str(
            self.f_4535149732094779661)
        res += '\tf_581203445514181141 = %s ,\n' % str(
            self.f_581203445514181141)
        res += '\tf_7567046777643367421 = %s ,\n' % str(
            self.f_7567046777643367421)
        res += '\tf_7818271317935764546 = %s ,\n' % str(
            self.f_7818271317935764546)
        res += '\tf_1449988654089269400 = %s ,\n' % str(
            self.f_1449988654089269400)
        res += '\tf_8538332288708448876 = %s ,\n' % str(
            self.f_8538332288708448876)
        res += '\tf_8660001712953173509 = %s ,\n' % str(
            self.f_8660001712953173509)
        res += '\tf_2401380060870497267 = %s ,\n' % str(
            self.f_2401380060870497267)
        res += '\tf_3913792219024292053 = %s ,\n' % str(
            self.f_3913792219024292053)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 34

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_6920772091196212887(self):
        return self.__f_6920772091196212887

    def __set_f_6920772091196212887(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_6920772091196212887 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1851582658599760477(self):
        return self.__f_1851582658599760477

    def __set_f_1851582658599760477(self, value):

        assert (isinstance(value, (int, CCRSET)))
        self.__f_1851582658599760477 = value if isinstance(
            value, CCRSET) else CCRSET(value)

    def __get_f_4535149732094779661(self):
        return self.__f_4535149732094779661

    def __set_f_4535149732094779661(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_4535149732094779661 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_581203445514181141(self):
        return self.__f_581203445514181141

    def __set_f_581203445514181141(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_581203445514181141 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_7567046777643367421(self):
        return self.__f_7567046777643367421

    def __set_f_7567046777643367421(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_7567046777643367421 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_7818271317935764546(self):
        return self.__f_7818271317935764546

    def __set_f_7818271317935764546(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_7818271317935764546 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_1449988654089269400(self):
        return self.__f_1449988654089269400

    def __set_f_1449988654089269400(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1449988654089269400 = int(value)

    def __get_f_8538332288708448876(self):
        return self.__f_8538332288708448876

    def __set_f_8538332288708448876(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8538332288708448876 = int(value)

    def __get_f_8660001712953173509(self):
        return self.__f_8660001712953173509

    def __set_f_8660001712953173509(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8660001712953173509 = int(value)

    def __get_f_2401380060870497267(self):
        return self.__f_2401380060870497267

    def __set_f_2401380060870497267(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_2401380060870497267 = int(value)

    def __get_f_3913792219024292053(self):
        return self.__f_3913792219024292053

    def __set_f_3913792219024292053(self, value):

        assert (isinstance(value, (int, PRECISION)))
        self.__f_3913792219024292053 = value if isinstance(
            value, PRECISION) else PRECISION(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_6920772091196212887 = property(__get_f_6920772091196212887,
                                     __set_f_6920772091196212887)
    f_1851582658599760477 = property(__get_f_1851582658599760477,
                                     __set_f_1851582658599760477)
    f_4535149732094779661 = property(__get_f_4535149732094779661,
                                     __set_f_4535149732094779661)
    f_581203445514181141 = property(__get_f_581203445514181141,
                                    __set_f_581203445514181141)
    f_7567046777643367421 = property(__get_f_7567046777643367421,
                                     __set_f_7567046777643367421)
    f_7818271317935764546 = property(__get_f_7818271317935764546,
                                     __set_f_7818271317935764546)
    f_1449988654089269400 = property(__get_f_1449988654089269400,
                                     __set_f_1449988654089269400)
    f_8538332288708448876 = property(__get_f_8538332288708448876,
                                     __set_f_8538332288708448876)
    f_8660001712953173509 = property(__get_f_8660001712953173509,
                                     __set_f_8660001712953173509)
    f_2401380060870497267 = property(__get_f_2401380060870497267,
                                     __set_f_2401380060870497267)
    f_3913792219024292053 = property(__get_f_3913792219024292053,
                                     __set_f_3913792219024292053)


class inst_i_2506286750019430415(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_6920772091196212887: [CCRCLR, 8]  # type: ignore
    __f_1851582658599760477: [CCRSET, 11]  # type: ignore
    __f_4535149732094779661: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_581203445514181141: [ADDR_GLB_8_WITH_BANK, 25]  # type: ignore
    __f_7567046777643367421: [STRIDE_GLB, 64]  # type: ignore
    __f_7818271317935764546: [STRIDE_GLB, 64]  # type: ignore
    __f_1449988654089269400: [datatype.uint16, 16]  # type: ignore
    __f_8538332288708448876: [datatype.uint16, 16]  # type: ignore
    __f_8660001712953173509: [datatype.uint16, 16]  # type: ignore
    __f_2401380060870497267: [datatype.uint16, 16]  # type: ignore
    __f_3913792219024292053: [PRECISION, 2]  # type: ignore
    __f_8182503352642059000: [MFU_TRANS_PERMUTE, 5]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[CCRCLR, CCRSET, ADDR_GLB_8_WITH_BANK,
                               ADDR_GLB_8_WITH_BANK, STRIDE_GLB, STRIDE_GLB,
                               int, int, int, int, PRECISION,
                               MFU_TRANS_PERMUTE,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        cf_str += 'p' + str(4)

        self.__f_8182503352642059000 = MFU_TRANS_PERMUTE(0)
        cf_str += '>u5'
        self.__f_3913792219024292053 = PRECISION(0)
        cf_str += '>u2'
        self.__f_2401380060870497267 = int(0)
        cf_str += '>u16'
        self.__f_8660001712953173509 = int(0)
        cf_str += '>u16'
        self.__f_8538332288708448876 = int(0)
        cf_str += '>u16'
        self.__f_1449988654089269400 = int(0)
        cf_str += '>u16'
        self.__f_7818271317935764546 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_7567046777643367421 = STRIDE_GLB(0)
        cf_str += '>u64'
        self.__f_581203445514181141 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_4535149732094779661 = ADDR_GLB_8_WITH_BANK(0)
        cf_str += '>u25'
        self.__f_1851582658599760477 = CCRSET(0)
        cf_str += '>u11'
        self.__f_6920772091196212887 = CCRCLR(0)
        cf_str += '>u8'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(144)

    def fields(
        self,
        f_6920772091196212887: CCRCLR = None,
        f_1851582658599760477: CCRSET = None,
        f_4535149732094779661: ADDR_GLB_8_WITH_BANK = None,
        f_581203445514181141: ADDR_GLB_8_WITH_BANK = None,
        f_7567046777643367421: STRIDE_GLB = None,
        f_7818271317935764546: STRIDE_GLB = None,
        f_1449988654089269400: int = None,
        f_8538332288708448876: int = None,
        f_8660001712953173509: int = None,
        f_2401380060870497267: int = None,
        f_3913792219024292053: PRECISION = None,
        f_8182503352642059000: MFU_TRANS_PERMUTE = None,
    ):
        if f_6920772091196212887:
            self.f_6920772091196212887 = f_6920772091196212887
        if f_1851582658599760477:
            self.f_1851582658599760477 = f_1851582658599760477
        if f_4535149732094779661:
            self.f_4535149732094779661 = f_4535149732094779661
        if f_581203445514181141:
            self.f_581203445514181141 = f_581203445514181141
        if f_7567046777643367421:
            self.f_7567046777643367421 = f_7567046777643367421
        if f_7818271317935764546:
            self.f_7818271317935764546 = f_7818271317935764546
        if f_1449988654089269400:
            self.f_1449988654089269400 = f_1449988654089269400
        if f_8538332288708448876:
            self.f_8538332288708448876 = f_8538332288708448876
        if f_8660001712953173509:
            self.f_8660001712953173509 = f_8660001712953173509
        if f_2401380060870497267:
            self.f_2401380060870497267 = f_2401380060870497267
        if f_3913792219024292053:
            self.f_3913792219024292053 = f_3913792219024292053
        if f_8182503352642059000:
            self.f_8182503352642059000 = f_8182503352642059000
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_8182503352642059000),
            int(self.f_3913792219024292053),
            int(self.f_2401380060870497267),
            int(self.f_8660001712953173509),
            int(self.f_8538332288708448876),
            int(self.f_1449988654089269400),
            int(self.f_7818271317935764546),
            int(self.f_7567046777643367421),
            int(self.f_581203445514181141),
            int(self.f_4535149732094779661),
            int(self.f_1851582658599760477),
            int(self.f_6920772091196212887),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 35
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x90
        (
            self.f_8182503352642059000,
            self.f_3913792219024292053,
            self.f_2401380060870497267,
            self.f_8660001712953173509,
            self.f_8538332288708448876,
            self.f_1449988654089269400,
            self.f_7818271317935764546,
            self.f_7567046777643367421,
            self.f_581203445514181141,
            self.f_4535149732094779661,
            self.f_1851582658599760477,
            self.f_6920772091196212887,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_2506286750019430415(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_2506286750019430415().fields(\n'
        res += '\tf_6920772091196212887 = %s ,\n' % str(
            self.f_6920772091196212887)
        res += '\tf_1851582658599760477 = %s ,\n' % str(
            self.f_1851582658599760477)
        res += '\tf_4535149732094779661 = %s ,\n' % str(
            self.f_4535149732094779661)
        res += '\tf_581203445514181141 = %s ,\n' % str(
            self.f_581203445514181141)
        res += '\tf_7567046777643367421 = %s ,\n' % str(
            self.f_7567046777643367421)
        res += '\tf_7818271317935764546 = %s ,\n' % str(
            self.f_7818271317935764546)
        res += '\tf_1449988654089269400 = %s ,\n' % str(
            self.f_1449988654089269400)
        res += '\tf_8538332288708448876 = %s ,\n' % str(
            self.f_8538332288708448876)
        res += '\tf_8660001712953173509 = %s ,\n' % str(
            self.f_8660001712953173509)
        res += '\tf_2401380060870497267 = %s ,\n' % str(
            self.f_2401380060870497267)
        res += '\tf_3913792219024292053 = %s ,\n' % str(
            self.f_3913792219024292053)
        res += '\tf_8182503352642059000 = %s ,\n' % str(
            self.f_8182503352642059000)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 35

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_6920772091196212887(self):
        return self.__f_6920772091196212887

    def __set_f_6920772091196212887(self, value):

        assert (isinstance(value, (int, CCRCLR)))
        self.__f_6920772091196212887 = value if isinstance(
            value, CCRCLR) else CCRCLR(value)

    def __get_f_1851582658599760477(self):
        return self.__f_1851582658599760477

    def __set_f_1851582658599760477(self, value):

        assert (isinstance(value, (int, CCRSET)))
        self.__f_1851582658599760477 = value if isinstance(
            value, CCRSET) else CCRSET(value)

    def __get_f_4535149732094779661(self):
        return self.__f_4535149732094779661

    def __set_f_4535149732094779661(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_4535149732094779661 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_581203445514181141(self):
        return self.__f_581203445514181141

    def __set_f_581203445514181141(self, value):

        assert (isinstance(value, (int, ADDR_GLB_8_WITH_BANK)))
        self.__f_581203445514181141 = value if isinstance(
            value, ADDR_GLB_8_WITH_BANK) else ADDR_GLB_8_WITH_BANK(value)

    def __get_f_7567046777643367421(self):
        return self.__f_7567046777643367421

    def __set_f_7567046777643367421(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_7567046777643367421 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_7818271317935764546(self):
        return self.__f_7818271317935764546

    def __set_f_7818271317935764546(self, value):

        assert (isinstance(value, (int, STRIDE_GLB)))
        self.__f_7818271317935764546 = value if isinstance(
            value, STRIDE_GLB) else STRIDE_GLB(value)

    def __get_f_1449988654089269400(self):
        return self.__f_1449988654089269400

    def __set_f_1449988654089269400(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_1449988654089269400 = int(value)

    def __get_f_8538332288708448876(self):
        return self.__f_8538332288708448876

    def __set_f_8538332288708448876(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8538332288708448876 = int(value)

    def __get_f_8660001712953173509(self):
        return self.__f_8660001712953173509

    def __set_f_8660001712953173509(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_8660001712953173509 = int(value)

    def __get_f_2401380060870497267(self):
        return self.__f_2401380060870497267

    def __set_f_2401380060870497267(self, value):
        assert int(value) < 2**16

        assert int(value) >= 0

        self.__f_2401380060870497267 = int(value)

    def __get_f_3913792219024292053(self):
        return self.__f_3913792219024292053

    def __set_f_3913792219024292053(self, value):

        assert (isinstance(value, (int, PRECISION)))
        self.__f_3913792219024292053 = value if isinstance(
            value, PRECISION) else PRECISION(value)

    def __get_f_8182503352642059000(self):
        return self.__f_8182503352642059000

    def __set_f_8182503352642059000(self, value):

        assert (isinstance(value, (int, MFU_TRANS_PERMUTE)))
        self.__f_8182503352642059000 = value if isinstance(
            value, MFU_TRANS_PERMUTE) else MFU_TRANS_PERMUTE(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_6920772091196212887 = property(__get_f_6920772091196212887,
                                     __set_f_6920772091196212887)
    f_1851582658599760477 = property(__get_f_1851582658599760477,
                                     __set_f_1851582658599760477)
    f_4535149732094779661 = property(__get_f_4535149732094779661,
                                     __set_f_4535149732094779661)
    f_581203445514181141 = property(__get_f_581203445514181141,
                                    __set_f_581203445514181141)
    f_7567046777643367421 = property(__get_f_7567046777643367421,
                                     __set_f_7567046777643367421)
    f_7818271317935764546 = property(__get_f_7818271317935764546,
                                     __set_f_7818271317935764546)
    f_1449988654089269400 = property(__get_f_1449988654089269400,
                                     __set_f_1449988654089269400)
    f_8538332288708448876 = property(__get_f_8538332288708448876,
                                     __set_f_8538332288708448876)
    f_8660001712953173509 = property(__get_f_8660001712953173509,
                                     __set_f_8660001712953173509)
    f_2401380060870497267 = property(__get_f_2401380060870497267,
                                     __set_f_2401380060870497267)
    f_3913792219024292053 = property(__get_f_3913792219024292053,
                                     __set_f_3913792219024292053)
    f_8182503352642059000 = property(__get_f_8182503352642059000,
                                     __set_f_8182503352642059000)


class inst_i_245645227484541732(serialize_struct):

    __f_2886468954866643279: [OPCODE, 8]  # type: ignore
    __f_7069821409202685498: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_3884497537755933089: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_3456041896755308975: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_1235145126119211769: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_7233042213142521317: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_7817033264319953673: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_1935873662097799787: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_6517932706035520941: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_6109244766921510246: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_7602708203520367839: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_8484916312572841017: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_7475577726134613608: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_3080396748317583134: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_4805479156552916396: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_2226523717988507933: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_6880128608303220015: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_7929548391703265546: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_1890389741247037704: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_8089000526326249960: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_4215934206796864118: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_8263114350448266781: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_3105726342457351282: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_9155335457014821664: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_1874447848080582962: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_2421150510568670761: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_8864203643479231408: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_7515089139502435038: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_6454158024196654905: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_7912124855558920198: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_3679437951771802611: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_8247842566306324845: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_8158374901270398197: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_4295321042938319819: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_7272080714498690751: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_8156112294546180618: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_2674416632986464345: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_960644645667862500: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_4679437111583321527: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_7750168364600150809: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_781249942706080297: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_7291861593943719631: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_6540698051607095838: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_7106828484281518527: [MFU_MN_PORTIN, 6]  # type: ignore
    __f_2807884874452250139: [MFU_MN_PORTIN, 6]  # type: ignore

    def __init__(self,
                 value: Union[bytes, str] = None,
                 fields: Tuple[MFU_MN_PORTIN, MFU_MN_PORTIN, MFU_MN_PORTIN,
                               MFU_MN_PORTIN, MFU_MN_PORTIN, MFU_MN_PORTIN,
                               MFU_MN_PORTIN, MFU_MN_PORTIN, MFU_MN_PORTIN,
                               MFU_MN_PORTIN, MFU_MN_PORTIN, MFU_MN_PORTIN,
                               MFU_MN_PORTIN, MFU_MN_PORTIN, MFU_MN_PORTIN,
                               MFU_MN_PORTIN, MFU_MN_PORTIN, MFU_MN_PORTIN,
                               MFU_MN_PORTIN, MFU_MN_PORTIN, MFU_MN_PORTIN,
                               MFU_MN_PORTIN, MFU_MN_PORTIN, MFU_MN_PORTIN,
                               MFU_MN_PORTIN, MFU_MN_PORTIN, MFU_MN_PORTIN,
                               MFU_MN_PORTIN, MFU_MN_PORTIN, MFU_MN_PORTIN,
                               MFU_MN_PORTIN, MFU_MN_PORTIN, MFU_MN_PORTIN,
                               MFU_MN_PORTIN, MFU_MN_PORTIN, MFU_MN_PORTIN,
                               MFU_MN_PORTIN, MFU_MN_PORTIN, MFU_MN_PORTIN,
                               MFU_MN_PORTIN, MFU_MN_PORTIN, MFU_MN_PORTIN,
                               MFU_MN_PORTIN, MFU_MN_PORTIN,] = None,
                 hooks=None) -> None:
        super().__init__(hooks)
        cf_str = ''

        self.__f_2807884874452250139 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_7106828484281518527 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_6540698051607095838 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_7291861593943719631 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_781249942706080297 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_7750168364600150809 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_4679437111583321527 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_960644645667862500 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_2674416632986464345 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_8156112294546180618 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_7272080714498690751 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_4295321042938319819 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_8158374901270398197 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_8247842566306324845 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_3679437951771802611 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_7912124855558920198 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_6454158024196654905 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_7515089139502435038 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_8864203643479231408 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_2421150510568670761 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_1874447848080582962 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_9155335457014821664 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_3105726342457351282 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_8263114350448266781 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_4215934206796864118 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_8089000526326249960 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_1890389741247037704 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_7929548391703265546 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_6880128608303220015 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_2226523717988507933 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_4805479156552916396 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_3080396748317583134 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_7475577726134613608 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_8484916312572841017 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_7602708203520367839 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_6109244766921510246 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_6517932706035520941 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_1935873662097799787 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_7817033264319953673 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_7233042213142521317 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_1235145126119211769 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_3456041896755308975 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_3884497537755933089 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_7069821409202685498 = MFU_MN_PORTIN(0)
        cf_str += '>u6'
        self.__f_2886468954866643279 = OPCODE(0)
        cf_str += '>u8'

        cf_str += '>'
        self.cf = bitstruct.compile(cf_str)
        self._cf_str = cf_str

        if isinstance(value, bytes):
            self.unpack(value)
        elif isinstance(value, str):
            try:
                h = binascii.unhexlify(value)
            except ValueError:
                h = None
            if h:
                self.unpack(h)
            else:
                self.deserialize(h)

        if fields is not None:
            self.fields(fields)

        self.opcode = OPCODE(145)

    def fields(
        self,
        f_7069821409202685498: MFU_MN_PORTIN = None,
        f_3884497537755933089: MFU_MN_PORTIN = None,
        f_3456041896755308975: MFU_MN_PORTIN = None,
        f_1235145126119211769: MFU_MN_PORTIN = None,
        f_7233042213142521317: MFU_MN_PORTIN = None,
        f_7817033264319953673: MFU_MN_PORTIN = None,
        f_1935873662097799787: MFU_MN_PORTIN = None,
        f_6517932706035520941: MFU_MN_PORTIN = None,
        f_6109244766921510246: MFU_MN_PORTIN = None,
        f_7602708203520367839: MFU_MN_PORTIN = None,
        f_8484916312572841017: MFU_MN_PORTIN = None,
        f_7475577726134613608: MFU_MN_PORTIN = None,
        f_3080396748317583134: MFU_MN_PORTIN = None,
        f_4805479156552916396: MFU_MN_PORTIN = None,
        f_2226523717988507933: MFU_MN_PORTIN = None,
        f_6880128608303220015: MFU_MN_PORTIN = None,
        f_7929548391703265546: MFU_MN_PORTIN = None,
        f_1890389741247037704: MFU_MN_PORTIN = None,
        f_8089000526326249960: MFU_MN_PORTIN = None,
        f_4215934206796864118: MFU_MN_PORTIN = None,
        f_8263114350448266781: MFU_MN_PORTIN = None,
        f_3105726342457351282: MFU_MN_PORTIN = None,
        f_9155335457014821664: MFU_MN_PORTIN = None,
        f_1874447848080582962: MFU_MN_PORTIN = None,
        f_2421150510568670761: MFU_MN_PORTIN = None,
        f_8864203643479231408: MFU_MN_PORTIN = None,
        f_7515089139502435038: MFU_MN_PORTIN = None,
        f_6454158024196654905: MFU_MN_PORTIN = None,
        f_7912124855558920198: MFU_MN_PORTIN = None,
        f_3679437951771802611: MFU_MN_PORTIN = None,
        f_8247842566306324845: MFU_MN_PORTIN = None,
        f_8158374901270398197: MFU_MN_PORTIN = None,
        f_4295321042938319819: MFU_MN_PORTIN = None,
        f_7272080714498690751: MFU_MN_PORTIN = None,
        f_8156112294546180618: MFU_MN_PORTIN = None,
        f_2674416632986464345: MFU_MN_PORTIN = None,
        f_960644645667862500: MFU_MN_PORTIN = None,
        f_4679437111583321527: MFU_MN_PORTIN = None,
        f_7750168364600150809: MFU_MN_PORTIN = None,
        f_781249942706080297: MFU_MN_PORTIN = None,
        f_7291861593943719631: MFU_MN_PORTIN = None,
        f_6540698051607095838: MFU_MN_PORTIN = None,
        f_7106828484281518527: MFU_MN_PORTIN = None,
        f_2807884874452250139: MFU_MN_PORTIN = None,
    ):
        if f_7069821409202685498:
            self.f_7069821409202685498 = f_7069821409202685498
        if f_3884497537755933089:
            self.f_3884497537755933089 = f_3884497537755933089
        if f_3456041896755308975:
            self.f_3456041896755308975 = f_3456041896755308975
        if f_1235145126119211769:
            self.f_1235145126119211769 = f_1235145126119211769
        if f_7233042213142521317:
            self.f_7233042213142521317 = f_7233042213142521317
        if f_7817033264319953673:
            self.f_7817033264319953673 = f_7817033264319953673
        if f_1935873662097799787:
            self.f_1935873662097799787 = f_1935873662097799787
        if f_6517932706035520941:
            self.f_6517932706035520941 = f_6517932706035520941
        if f_6109244766921510246:
            self.f_6109244766921510246 = f_6109244766921510246
        if f_7602708203520367839:
            self.f_7602708203520367839 = f_7602708203520367839
        if f_8484916312572841017:
            self.f_8484916312572841017 = f_8484916312572841017
        if f_7475577726134613608:
            self.f_7475577726134613608 = f_7475577726134613608
        if f_3080396748317583134:
            self.f_3080396748317583134 = f_3080396748317583134
        if f_4805479156552916396:
            self.f_4805479156552916396 = f_4805479156552916396
        if f_2226523717988507933:
            self.f_2226523717988507933 = f_2226523717988507933
        if f_6880128608303220015:
            self.f_6880128608303220015 = f_6880128608303220015
        if f_7929548391703265546:
            self.f_7929548391703265546 = f_7929548391703265546
        if f_1890389741247037704:
            self.f_1890389741247037704 = f_1890389741247037704
        if f_8089000526326249960:
            self.f_8089000526326249960 = f_8089000526326249960
        if f_4215934206796864118:
            self.f_4215934206796864118 = f_4215934206796864118
        if f_8263114350448266781:
            self.f_8263114350448266781 = f_8263114350448266781
        if f_3105726342457351282:
            self.f_3105726342457351282 = f_3105726342457351282
        if f_9155335457014821664:
            self.f_9155335457014821664 = f_9155335457014821664
        if f_1874447848080582962:
            self.f_1874447848080582962 = f_1874447848080582962
        if f_2421150510568670761:
            self.f_2421150510568670761 = f_2421150510568670761
        if f_8864203643479231408:
            self.f_8864203643479231408 = f_8864203643479231408
        if f_7515089139502435038:
            self.f_7515089139502435038 = f_7515089139502435038
        if f_6454158024196654905:
            self.f_6454158024196654905 = f_6454158024196654905
        if f_7912124855558920198:
            self.f_7912124855558920198 = f_7912124855558920198
        if f_3679437951771802611:
            self.f_3679437951771802611 = f_3679437951771802611
        if f_8247842566306324845:
            self.f_8247842566306324845 = f_8247842566306324845
        if f_8158374901270398197:
            self.f_8158374901270398197 = f_8158374901270398197
        if f_4295321042938319819:
            self.f_4295321042938319819 = f_4295321042938319819
        if f_7272080714498690751:
            self.f_7272080714498690751 = f_7272080714498690751
        if f_8156112294546180618:
            self.f_8156112294546180618 = f_8156112294546180618
        if f_2674416632986464345:
            self.f_2674416632986464345 = f_2674416632986464345
        if f_960644645667862500:
            self.f_960644645667862500 = f_960644645667862500
        if f_4679437111583321527:
            self.f_4679437111583321527 = f_4679437111583321527
        if f_7750168364600150809:
            self.f_7750168364600150809 = f_7750168364600150809
        if f_781249942706080297:
            self.f_781249942706080297 = f_781249942706080297
        if f_7291861593943719631:
            self.f_7291861593943719631 = f_7291861593943719631
        if f_6540698051607095838:
            self.f_6540698051607095838 = f_6540698051607095838
        if f_7106828484281518527:
            self.f_7106828484281518527 = f_7106828484281518527
        if f_2807884874452250139:
            self.f_2807884874452250139 = f_2807884874452250139
        return self

    def pack(self) -> bytes:
        return self.cf.pack(
            int(self.f_2807884874452250139),
            int(self.f_7106828484281518527),
            int(self.f_6540698051607095838),
            int(self.f_7291861593943719631),
            int(self.f_781249942706080297),
            int(self.f_7750168364600150809),
            int(self.f_4679437111583321527),
            int(self.f_960644645667862500),
            int(self.f_2674416632986464345),
            int(self.f_8156112294546180618),
            int(self.f_7272080714498690751),
            int(self.f_4295321042938319819),
            int(self.f_8158374901270398197),
            int(self.f_8247842566306324845),
            int(self.f_3679437951771802611),
            int(self.f_7912124855558920198),
            int(self.f_6454158024196654905),
            int(self.f_7515089139502435038),
            int(self.f_8864203643479231408),
            int(self.f_2421150510568670761),
            int(self.f_1874447848080582962),
            int(self.f_9155335457014821664),
            int(self.f_3105726342457351282),
            int(self.f_8263114350448266781),
            int(self.f_4215934206796864118),
            int(self.f_8089000526326249960),
            int(self.f_1890389741247037704),
            int(self.f_7929548391703265546),
            int(self.f_6880128608303220015),
            int(self.f_2226523717988507933),
            int(self.f_4805479156552916396),
            int(self.f_3080396748317583134),
            int(self.f_7475577726134613608),
            int(self.f_8484916312572841017),
            int(self.f_7602708203520367839),
            int(self.f_6109244766921510246),
            int(self.f_6517932706035520941),
            int(self.f_1935873662097799787),
            int(self.f_7817033264319953673),
            int(self.f_7233042213142521317),
            int(self.f_1235145126119211769),
            int(self.f_3456041896755308975),
            int(self.f_3884497537755933089),
            int(self.f_7069821409202685498),
            int(self.f_2886468954866643279),
        )[::-1]

    def unpack(self, data: bytes):
        assert len(data) == 34
        res = self.cf.unpack(data[::-1])
        assert res[-1] == 0x91
        (
            self.f_2807884874452250139,
            self.f_7106828484281518527,
            self.f_6540698051607095838,
            self.f_7291861593943719631,
            self.f_781249942706080297,
            self.f_7750168364600150809,
            self.f_4679437111583321527,
            self.f_960644645667862500,
            self.f_2674416632986464345,
            self.f_8156112294546180618,
            self.f_7272080714498690751,
            self.f_4295321042938319819,
            self.f_8158374901270398197,
            self.f_8247842566306324845,
            self.f_3679437951771802611,
            self.f_7912124855558920198,
            self.f_6454158024196654905,
            self.f_7515089139502435038,
            self.f_8864203643479231408,
            self.f_2421150510568670761,
            self.f_1874447848080582962,
            self.f_9155335457014821664,
            self.f_3105726342457351282,
            self.f_8263114350448266781,
            self.f_4215934206796864118,
            self.f_8089000526326249960,
            self.f_1890389741247037704,
            self.f_7929548391703265546,
            self.f_6880128608303220015,
            self.f_2226523717988507933,
            self.f_4805479156552916396,
            self.f_3080396748317583134,
            self.f_7475577726134613608,
            self.f_8484916312572841017,
            self.f_7602708203520367839,
            self.f_6109244766921510246,
            self.f_6517932706035520941,
            self.f_1935873662097799787,
            self.f_7817033264319953673,
            self.f_7233042213142521317,
            self.f_1235145126119211769,
            self.f_3456041896755308975,
            self.f_3884497537755933089,
            self.f_7069821409202685498,
            self.f_2886468954866643279,
        ) = res

    def __repr__(self):
        return 'inst_i_245645227484541732(\'' + self.pack().hex() + '\')'

    def __str__(self):
        res = 'inst_i_245645227484541732().fields(\n'
        res += '\tf_7069821409202685498 = %s ,\n' % str(
            self.f_7069821409202685498)
        res += '\tf_3884497537755933089 = %s ,\n' % str(
            self.f_3884497537755933089)
        res += '\tf_3456041896755308975 = %s ,\n' % str(
            self.f_3456041896755308975)
        res += '\tf_1235145126119211769 = %s ,\n' % str(
            self.f_1235145126119211769)
        res += '\tf_7233042213142521317 = %s ,\n' % str(
            self.f_7233042213142521317)
        res += '\tf_7817033264319953673 = %s ,\n' % str(
            self.f_7817033264319953673)
        res += '\tf_1935873662097799787 = %s ,\n' % str(
            self.f_1935873662097799787)
        res += '\tf_6517932706035520941 = %s ,\n' % str(
            self.f_6517932706035520941)
        res += '\tf_6109244766921510246 = %s ,\n' % str(
            self.f_6109244766921510246)
        res += '\tf_7602708203520367839 = %s ,\n' % str(
            self.f_7602708203520367839)
        res += '\tf_8484916312572841017 = %s ,\n' % str(
            self.f_8484916312572841017)
        res += '\tf_7475577726134613608 = %s ,\n' % str(
            self.f_7475577726134613608)
        res += '\tf_3080396748317583134 = %s ,\n' % str(
            self.f_3080396748317583134)
        res += '\tf_4805479156552916396 = %s ,\n' % str(
            self.f_4805479156552916396)
        res += '\tf_2226523717988507933 = %s ,\n' % str(
            self.f_2226523717988507933)
        res += '\tf_6880128608303220015 = %s ,\n' % str(
            self.f_6880128608303220015)
        res += '\tf_7929548391703265546 = %s ,\n' % str(
            self.f_7929548391703265546)
        res += '\tf_1890389741247037704 = %s ,\n' % str(
            self.f_1890389741247037704)
        res += '\tf_8089000526326249960 = %s ,\n' % str(
            self.f_8089000526326249960)
        res += '\tf_4215934206796864118 = %s ,\n' % str(
            self.f_4215934206796864118)
        res += '\tf_8263114350448266781 = %s ,\n' % str(
            self.f_8263114350448266781)
        res += '\tf_3105726342457351282 = %s ,\n' % str(
            self.f_3105726342457351282)
        res += '\tf_9155335457014821664 = %s ,\n' % str(
            self.f_9155335457014821664)
        res += '\tf_1874447848080582962 = %s ,\n' % str(
            self.f_1874447848080582962)
        res += '\tf_2421150510568670761 = %s ,\n' % str(
            self.f_2421150510568670761)
        res += '\tf_8864203643479231408 = %s ,\n' % str(
            self.f_8864203643479231408)
        res += '\tf_7515089139502435038 = %s ,\n' % str(
            self.f_7515089139502435038)
        res += '\tf_6454158024196654905 = %s ,\n' % str(
            self.f_6454158024196654905)
        res += '\tf_7912124855558920198 = %s ,\n' % str(
            self.f_7912124855558920198)
        res += '\tf_3679437951771802611 = %s ,\n' % str(
            self.f_3679437951771802611)
        res += '\tf_8247842566306324845 = %s ,\n' % str(
            self.f_8247842566306324845)
        res += '\tf_8158374901270398197 = %s ,\n' % str(
            self.f_8158374901270398197)
        res += '\tf_4295321042938319819 = %s ,\n' % str(
            self.f_4295321042938319819)
        res += '\tf_7272080714498690751 = %s ,\n' % str(
            self.f_7272080714498690751)
        res += '\tf_8156112294546180618 = %s ,\n' % str(
            self.f_8156112294546180618)
        res += '\tf_2674416632986464345 = %s ,\n' % str(
            self.f_2674416632986464345)
        res += '\tf_960644645667862500 = %s ,\n' % str(
            self.f_960644645667862500)
        res += '\tf_4679437111583321527 = %s ,\n' % str(
            self.f_4679437111583321527)
        res += '\tf_7750168364600150809 = %s ,\n' % str(
            self.f_7750168364600150809)
        res += '\tf_781249942706080297 = %s ,\n' % str(
            self.f_781249942706080297)
        res += '\tf_7291861593943719631 = %s ,\n' % str(
            self.f_7291861593943719631)
        res += '\tf_6540698051607095838 = %s ,\n' % str(
            self.f_6540698051607095838)
        res += '\tf_7106828484281518527 = %s ,\n' % str(
            self.f_7106828484281518527)
        res += '\tf_2807884874452250139 = %s ,\n' % str(
            self.f_2807884874452250139)
        res += ')'
        return res

    def deserialize(self, data: str):
        pass

    @classmethod
    def total_bytes(cls):
        return 34

    # getter and setters

    def __get_f_2886468954866643279(self):
        return self.__f_2886468954866643279

    def __set_f_2886468954866643279(self, value):

        assert (isinstance(value, (int, OPCODE)))
        self.__f_2886468954866643279 = value if isinstance(
            value, OPCODE) else OPCODE(value)

    def __get_f_7069821409202685498(self):
        return self.__f_7069821409202685498

    def __set_f_7069821409202685498(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_7069821409202685498 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_3884497537755933089(self):
        return self.__f_3884497537755933089

    def __set_f_3884497537755933089(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_3884497537755933089 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_3456041896755308975(self):
        return self.__f_3456041896755308975

    def __set_f_3456041896755308975(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_3456041896755308975 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_1235145126119211769(self):
        return self.__f_1235145126119211769

    def __set_f_1235145126119211769(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_1235145126119211769 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_7233042213142521317(self):
        return self.__f_7233042213142521317

    def __set_f_7233042213142521317(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_7233042213142521317 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_7817033264319953673(self):
        return self.__f_7817033264319953673

    def __set_f_7817033264319953673(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_7817033264319953673 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_1935873662097799787(self):
        return self.__f_1935873662097799787

    def __set_f_1935873662097799787(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_1935873662097799787 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_6517932706035520941(self):
        return self.__f_6517932706035520941

    def __set_f_6517932706035520941(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_6517932706035520941 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_6109244766921510246(self):
        return self.__f_6109244766921510246

    def __set_f_6109244766921510246(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_6109244766921510246 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_7602708203520367839(self):
        return self.__f_7602708203520367839

    def __set_f_7602708203520367839(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_7602708203520367839 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_8484916312572841017(self):
        return self.__f_8484916312572841017

    def __set_f_8484916312572841017(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_8484916312572841017 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_7475577726134613608(self):
        return self.__f_7475577726134613608

    def __set_f_7475577726134613608(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_7475577726134613608 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_3080396748317583134(self):
        return self.__f_3080396748317583134

    def __set_f_3080396748317583134(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_3080396748317583134 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_4805479156552916396(self):
        return self.__f_4805479156552916396

    def __set_f_4805479156552916396(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_4805479156552916396 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_2226523717988507933(self):
        return self.__f_2226523717988507933

    def __set_f_2226523717988507933(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_2226523717988507933 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_6880128608303220015(self):
        return self.__f_6880128608303220015

    def __set_f_6880128608303220015(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_6880128608303220015 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_7929548391703265546(self):
        return self.__f_7929548391703265546

    def __set_f_7929548391703265546(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_7929548391703265546 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_1890389741247037704(self):
        return self.__f_1890389741247037704

    def __set_f_1890389741247037704(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_1890389741247037704 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_8089000526326249960(self):
        return self.__f_8089000526326249960

    def __set_f_8089000526326249960(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_8089000526326249960 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_4215934206796864118(self):
        return self.__f_4215934206796864118

    def __set_f_4215934206796864118(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_4215934206796864118 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_8263114350448266781(self):
        return self.__f_8263114350448266781

    def __set_f_8263114350448266781(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_8263114350448266781 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_3105726342457351282(self):
        return self.__f_3105726342457351282

    def __set_f_3105726342457351282(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_3105726342457351282 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_9155335457014821664(self):
        return self.__f_9155335457014821664

    def __set_f_9155335457014821664(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_9155335457014821664 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_1874447848080582962(self):
        return self.__f_1874447848080582962

    def __set_f_1874447848080582962(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_1874447848080582962 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_2421150510568670761(self):
        return self.__f_2421150510568670761

    def __set_f_2421150510568670761(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_2421150510568670761 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_8864203643479231408(self):
        return self.__f_8864203643479231408

    def __set_f_8864203643479231408(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_8864203643479231408 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_7515089139502435038(self):
        return self.__f_7515089139502435038

    def __set_f_7515089139502435038(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_7515089139502435038 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_6454158024196654905(self):
        return self.__f_6454158024196654905

    def __set_f_6454158024196654905(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_6454158024196654905 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_7912124855558920198(self):
        return self.__f_7912124855558920198

    def __set_f_7912124855558920198(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_7912124855558920198 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_3679437951771802611(self):
        return self.__f_3679437951771802611

    def __set_f_3679437951771802611(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_3679437951771802611 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_8247842566306324845(self):
        return self.__f_8247842566306324845

    def __set_f_8247842566306324845(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_8247842566306324845 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_8158374901270398197(self):
        return self.__f_8158374901270398197

    def __set_f_8158374901270398197(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_8158374901270398197 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_4295321042938319819(self):
        return self.__f_4295321042938319819

    def __set_f_4295321042938319819(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_4295321042938319819 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_7272080714498690751(self):
        return self.__f_7272080714498690751

    def __set_f_7272080714498690751(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_7272080714498690751 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_8156112294546180618(self):
        return self.__f_8156112294546180618

    def __set_f_8156112294546180618(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_8156112294546180618 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_2674416632986464345(self):
        return self.__f_2674416632986464345

    def __set_f_2674416632986464345(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_2674416632986464345 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_960644645667862500(self):
        return self.__f_960644645667862500

    def __set_f_960644645667862500(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_960644645667862500 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_4679437111583321527(self):
        return self.__f_4679437111583321527

    def __set_f_4679437111583321527(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_4679437111583321527 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_7750168364600150809(self):
        return self.__f_7750168364600150809

    def __set_f_7750168364600150809(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_7750168364600150809 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_781249942706080297(self):
        return self.__f_781249942706080297

    def __set_f_781249942706080297(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_781249942706080297 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_7291861593943719631(self):
        return self.__f_7291861593943719631

    def __set_f_7291861593943719631(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_7291861593943719631 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_6540698051607095838(self):
        return self.__f_6540698051607095838

    def __set_f_6540698051607095838(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_6540698051607095838 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_7106828484281518527(self):
        return self.__f_7106828484281518527

    def __set_f_7106828484281518527(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_7106828484281518527 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    def __get_f_2807884874452250139(self):
        return self.__f_2807884874452250139

    def __set_f_2807884874452250139(self, value):

        assert (isinstance(value, (int, MFU_MN_PORTIN)))
        self.__f_2807884874452250139 = value if isinstance(
            value, MFU_MN_PORTIN) else MFU_MN_PORTIN(value)

    f_2886468954866643279 = property(__get_f_2886468954866643279,
                                     __set_f_2886468954866643279)
    f_7069821409202685498 = property(__get_f_7069821409202685498,
                                     __set_f_7069821409202685498)
    f_3884497537755933089 = property(__get_f_3884497537755933089,
                                     __set_f_3884497537755933089)
    f_3456041896755308975 = property(__get_f_3456041896755308975,
                                     __set_f_3456041896755308975)
    f_1235145126119211769 = property(__get_f_1235145126119211769,
                                     __set_f_1235145126119211769)
    f_7233042213142521317 = property(__get_f_7233042213142521317,
                                     __set_f_7233042213142521317)
    f_7817033264319953673 = property(__get_f_7817033264319953673,
                                     __set_f_7817033264319953673)
    f_1935873662097799787 = property(__get_f_1935873662097799787,
                                     __set_f_1935873662097799787)
    f_6517932706035520941 = property(__get_f_6517932706035520941,
                                     __set_f_6517932706035520941)
    f_6109244766921510246 = property(__get_f_6109244766921510246,
                                     __set_f_6109244766921510246)
    f_7602708203520367839 = property(__get_f_7602708203520367839,
                                     __set_f_7602708203520367839)
    f_8484916312572841017 = property(__get_f_8484916312572841017,
                                     __set_f_8484916312572841017)
    f_7475577726134613608 = property(__get_f_7475577726134613608,
                                     __set_f_7475577726134613608)
    f_3080396748317583134 = property(__get_f_3080396748317583134,
                                     __set_f_3080396748317583134)
    f_4805479156552916396 = property(__get_f_4805479156552916396,
                                     __set_f_4805479156552916396)
    f_2226523717988507933 = property(__get_f_2226523717988507933,
                                     __set_f_2226523717988507933)
    f_6880128608303220015 = property(__get_f_6880128608303220015,
                                     __set_f_6880128608303220015)
    f_7929548391703265546 = property(__get_f_7929548391703265546,
                                     __set_f_7929548391703265546)
    f_1890389741247037704 = property(__get_f_1890389741247037704,
                                     __set_f_1890389741247037704)
    f_8089000526326249960 = property(__get_f_8089000526326249960,
                                     __set_f_8089000526326249960)
    f_4215934206796864118 = property(__get_f_4215934206796864118,
                                     __set_f_4215934206796864118)
    f_8263114350448266781 = property(__get_f_8263114350448266781,
                                     __set_f_8263114350448266781)
    f_3105726342457351282 = property(__get_f_3105726342457351282,
                                     __set_f_3105726342457351282)
    f_9155335457014821664 = property(__get_f_9155335457014821664,
                                     __set_f_9155335457014821664)
    f_1874447848080582962 = property(__get_f_1874447848080582962,
                                     __set_f_1874447848080582962)
    f_2421150510568670761 = property(__get_f_2421150510568670761,
                                     __set_f_2421150510568670761)
    f_8864203643479231408 = property(__get_f_8864203643479231408,
                                     __set_f_8864203643479231408)
    f_7515089139502435038 = property(__get_f_7515089139502435038,
                                     __set_f_7515089139502435038)
    f_6454158024196654905 = property(__get_f_6454158024196654905,
                                     __set_f_6454158024196654905)
    f_7912124855558920198 = property(__get_f_7912124855558920198,
                                     __set_f_7912124855558920198)
    f_3679437951771802611 = property(__get_f_3679437951771802611,
                                     __set_f_3679437951771802611)
    f_8247842566306324845 = property(__get_f_8247842566306324845,
                                     __set_f_8247842566306324845)
    f_8158374901270398197 = property(__get_f_8158374901270398197,
                                     __set_f_8158374901270398197)
    f_4295321042938319819 = property(__get_f_4295321042938319819,
                                     __set_f_4295321042938319819)
    f_7272080714498690751 = property(__get_f_7272080714498690751,
                                     __set_f_7272080714498690751)
    f_8156112294546180618 = property(__get_f_8156112294546180618,
                                     __set_f_8156112294546180618)
    f_2674416632986464345 = property(__get_f_2674416632986464345,
                                     __set_f_2674416632986464345)
    f_960644645667862500 = property(__get_f_960644645667862500,
                                    __set_f_960644645667862500)
    f_4679437111583321527 = property(__get_f_4679437111583321527,
                                     __set_f_4679437111583321527)
    f_7750168364600150809 = property(__get_f_7750168364600150809,
                                     __set_f_7750168364600150809)
    f_781249942706080297 = property(__get_f_781249942706080297,
                                    __set_f_781249942706080297)
    f_7291861593943719631 = property(__get_f_7291861593943719631,
                                     __set_f_7291861593943719631)
    f_6540698051607095838 = property(__get_f_6540698051607095838,
                                     __set_f_6540698051607095838)
    f_7106828484281518527 = property(__get_f_7106828484281518527,
                                     __set_f_7106828484281518527)
    f_2807884874452250139 = property(__get_f_2807884874452250139,
                                     __set_f_2807884874452250139)


property = OldProperty


############################
# auto generated decode
def decode_bytes_to_gnne_inst(ref: bytes):
    i = 0
    res = []
    offsets = []
    while i < len(ref):
        if ref[i] == 0:
            res.append(inst_i_6674109482354074040(ref[i:i + 1]))
            offsets.append(i)
            i = i + 1
            continue
        if ref[i] == 1:
            res.append(inst_i_304026372243538007(ref[i:i + 10]))
            offsets.append(i)
            i = i + 10
            continue
        if ref[i] == 2:
            res.append(inst_i_4723717955423805745(ref[i:i + 13]))
            offsets.append(i)
            i = i + 13
            continue
        if ref[i] == 3:
            res.append(inst_i_328345304491746530(ref[i:i + 5]))
            offsets.append(i)
            i = i + 5
            continue
        if ref[i] == 4:
            res.append(inst_i_8790047992392043228(ref[i:i + 1]))
            offsets.append(i)
            i = i + 1
            continue
        if ref[i] == 5:
            res.append(inst_i_7155768076259033706(ref[i:i + 6]))
            offsets.append(i)
            i = i + 6
            continue
        if ref[i] == 8:
            res.append(inst_i_4539906387927636499(ref[i:i + 2]))
            offsets.append(i)
            i = i + 2
            continue
        if ref[i] == 16:
            res.append(inst_i_4968684677827927616(ref[i:i + 22]))
            offsets.append(i)
            i = i + 22
            continue
        if ref[i] == 17:
            res.append(inst_i_6647669131517538538(ref[i:i + 20]))
            offsets.append(i)
            i = i + 20
            continue
        if ref[i] == 18:
            res.append(inst_i_6703668108300758238(ref[i:i + 23]))
            offsets.append(i)
            i = i + 23
            continue
        if ref[i] == 20:
            res.append(inst_i_9152920230794971550(ref[i:i + 14]))
            offsets.append(i)
            i = i + 14
            continue
        if ref[i] == 21:
            res.append(inst_i_7204637145564182256(ref[i:i + 10]))
            offsets.append(i)
            i = i + 10
            continue
        if ref[i] == 32:
            res.append(inst_i_2089276022054688120(ref[i:i + 27]))
            offsets.append(i)
            i = i + 27
            continue
        if ref[i] == 33:
            res.append(inst_i_2841594760846416640(ref[i:i + 26]))
            offsets.append(i)
            i = i + 26
            continue
        if ref[i] == 34:
            res.append(inst_i_3414519735293012969(ref[i:i + 20]))
            offsets.append(i)
            i = i + 20
            continue
        if ref[i] == 36:
            res.append(inst_i_3246495767012874974(ref[i:i + 14]))
            offsets.append(i)
            i = i + 14
            continue
        if ref[i] == 37:
            res.append(inst_i_8339684182387014894(ref[i:i + 10]))
            offsets.append(i)
            i = i + 10
            continue
        if ref[i] == 65:
            res.append(inst_i_6868657659093990379(ref[i:i + 2]))
            offsets.append(i)
            i = i + 2
            continue
        if ref[i] == 66:
            res.append(inst_i_8430774666881311866(ref[i:i + 20]))
            offsets.append(i)
            i = i + 20
            continue
        if ref[i] == 67:
            res.append(inst_i_6471126574510039166(ref[i:i + 14]))
            offsets.append(i)
            i = i + 14
            continue
        if ref[i] == 68:
            res.append(inst_i_6369672458787877517(ref[i:i + 3]))
            offsets.append(i)
            i = i + 3
            continue
        if ref[i] == 69:
            res.append(inst_i_7025294518658670577(ref[i:i + 6]))
            offsets.append(i)
            i = i + 6
            continue
        if ref[i] == 70:
            res.append(inst_i_6731377247628139860(ref[i:i + 33]))
            offsets.append(i)
            i = i + 33
            continue
        if ref[i] == 71:
            res.append(inst_i_5088819369833811485(ref[i:i + 11]))
            offsets.append(i)
            i = i + 11
            continue
        if ref[i] == 72:
            res.append(inst_i_7758253786169375348(ref[i:i + 9]))
            offsets.append(i)
            i = i + 9
            continue
        if ref[i] == 73:
            res.append(inst_i_8336797519624639034(ref[i:i + 6]))
            offsets.append(i)
            i = i + 6
            continue
        if ref[i] == 74:
            res.append(inst_i_2090902360472978351(ref[i:i + 18]))
            offsets.append(i)
            i = i + 18
            continue
        if ref[i] == 75:
            res.append(inst_i_4164694345981782964(ref[i:i + 33]))
            offsets.append(i)
            i = i + 33
            continue
        if ref[i] == 76:
            res.append(inst_i_4473276217691097372(ref[i:i + 6]))
            offsets.append(i)
            i = i + 6
            continue
        if ref[i] == 77:
            res.append(inst_i_4137136459015411447(ref[i:i + 6]))
            offsets.append(i)
            i = i + 6
            continue
        if ref[i] == 79:
            res.append(inst_i_214212455253550760(ref[i:i + 5]))
            offsets.append(i)
            i = i + 5
            continue
        if ref[i] == 129:
            res.append(inst_i_7571105850837497638(ref[i:i + 36]))
            offsets.append(i)
            i = i + 36
            continue
        if ref[i] == 130:
            res.append(inst_i_4966324269173843223(ref[i:i + 16]))
            offsets.append(i)
            i = i + 16
            continue
        if ref[i] == 131:
            res.append(inst_i_6096737859014398957(ref[i:i + 31]))
            offsets.append(i)
            i = i + 31
            continue
        if ref[i] == 132:
            res.append(inst_i_4266661972367639294(ref[i:i + 21]))
            offsets.append(i)
            i = i + 21
            continue
        if ref[i] == 133:
            res.append(inst_i_1712250146653531835(ref[i:i + 30]))
            offsets.append(i)
            i = i + 30
            continue
        if ref[i] == 134:
            res.append(inst_i_447177514076795622(ref[i:i + 9]))
            offsets.append(i)
            i = i + 9
            continue
        if ref[i] == 135:
            res.append(inst_i_2656964308044352142(ref[i:i + 29]))
            offsets.append(i)
            i = i + 29
            continue
        if ref[i] == 136:
            res.append(inst_i_7317298242942939054(ref[i:i + 6]))
            offsets.append(i)
            i = i + 6
            continue
        if ref[i] == 137:
            res.append(inst_i_4940390838445604897(ref[i:i + 10]))
            offsets.append(i)
            i = i + 10
            continue
        if ref[i] == 138:
            res.append(inst_i_7071148236208088088(ref[i:i + 9]))
            offsets.append(i)
            i = i + 9
            continue
        if ref[i] == 139:
            res.append(inst_i_3215644467781021096(ref[i:i + 31]))
            offsets.append(i)
            i = i + 31
            continue
        if ref[i] == 140:
            res.append(inst_i_4300588898699658039(ref[i:i + 53]))
            offsets.append(i)
            i = i + 53
            continue
        if ref[i] == 141:
            res.append(inst_i_4573608092199809765(ref[i:i + 50]))
            offsets.append(i)
            i = i + 50
            continue
        if ref[i] == 142:
            res.append(inst_i_3562245241250454416(ref[i:i + 10]))
            offsets.append(i)
            i = i + 10
            continue
        if ref[i] == 143:
            res.append(inst_i_7361852897854452313(ref[i:i + 34]))
            offsets.append(i)
            i = i + 34
            continue
        if ref[i] == 144:
            res.append(inst_i_2506286750019430415(ref[i:i + 35]))
            offsets.append(i)
            i = i + 35
            continue
        if ref[i] == 145:
            res.append(inst_i_245645227484541732(ref[i:i + 34]))
            offsets.append(i)
            i = i + 34
            continue
        raise Exception('unknown opcode')
    return (res, offsets)
