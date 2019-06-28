from enum import Enum, unique


@unique
class LevelSystemEnum(Enum):
    HUNDRED = "百分制"
    FIVE = "五级制"
    TWO = "两级制"


@unique
class WebPageLevelSystemEnum(Enum):
    """ 当前录入界面的种类 """
    FIVE = "五级分制"
    TWO = "两级分制"


@unique
class FiveLevelSystemEnum(Enum):
    YOU_XIU = "优秀"
    LIANG_HAO = "良好"
    ZHONG_DENG = "中等"
    JI_GE = "及格"
    BU_JI_GE = "不及格"
    MIAN_XIU = "免修"
    HUAN_KAO = "缓考"
    QUE_KAO = "缺考"
    QU_XIAO_ZI_GE = "取消资格"


@unique
class TwoLevelSystemEnum(Enum):
    HE_GE = "合格"
    BU_HE_GE = "不合格"
    MIAN_XIU = "免修"
    HUAN_KAO = "缓考"
    QUE_KAO = "缺考"
    QU_XIAO_ZI_GE = "取消资格"


# 实际值 -> select值
FIVE_LEVEL_INPUT_MAP = {
    FiveLevelSystemEnum.YOU_XIU.value: FiveLevelSystemEnum.YOU_XIU.value,
    FiveLevelSystemEnum.LIANG_HAO.value: FiveLevelSystemEnum.LIANG_HAO.value,
    FiveLevelSystemEnum.ZHONG_DENG.value: FiveLevelSystemEnum.ZHONG_DENG.value,
    FiveLevelSystemEnum.JI_GE.value: FiveLevelSystemEnum.JI_GE.value,
    FiveLevelSystemEnum.BU_JI_GE.value: FiveLevelSystemEnum.BU_JI_GE.value,
    FiveLevelSystemEnum.MIAN_XIU.value: FiveLevelSystemEnum.MIAN_XIU.value,
    FiveLevelSystemEnum.HUAN_KAO.value: FiveLevelSystemEnum.HUAN_KAO.value,
    FiveLevelSystemEnum.QUE_KAO.value: FiveLevelSystemEnum.QUE_KAO.value,
    FiveLevelSystemEnum.QU_XIAO_ZI_GE.value: FiveLevelSystemEnum.QU_XIAO_ZI_GE.value
}

TWO_LEVEL_INPUT_MAP = {
    TwoLevelSystemEnum.HE_GE.value: TwoLevelSystemEnum.HE_GE.value,
    TwoLevelSystemEnum.BU_HE_GE.value: TwoLevelSystemEnum.BU_HE_GE.value,
    TwoLevelSystemEnum.MIAN_XIU.value: TwoLevelSystemEnum.MIAN_XIU.value,
    TwoLevelSystemEnum.HUAN_KAO.value: TwoLevelSystemEnum.HUAN_KAO.value,
    TwoLevelSystemEnum.QUE_KAO.value: TwoLevelSystemEnum.QUE_KAO.value,
    TwoLevelSystemEnum.QU_XIAO_ZI_GE.value: TwoLevelSystemEnum.QU_XIAO_ZI_GE.value
}

# 默认映射相等
# select 值 -> 映射值
FIVE_LEVEL_MAP = {
    FiveLevelSystemEnum.YOU_XIU.value: FiveLevelSystemEnum.YOU_XIU.value,
    FiveLevelSystemEnum.LIANG_HAO.value: FiveLevelSystemEnum.LIANG_HAO.value,
    FiveLevelSystemEnum.ZHONG_DENG.value: FiveLevelSystemEnum.ZHONG_DENG.value,
    FiveLevelSystemEnum.JI_GE.value: FiveLevelSystemEnum.JI_GE.value,
    FiveLevelSystemEnum.BU_JI_GE.value: FiveLevelSystemEnum.BU_JI_GE.value,
    FiveLevelSystemEnum.MIAN_XIU.value: FiveLevelSystemEnum.MIAN_XIU.value,
    FiveLevelSystemEnum.HUAN_KAO.value: FiveLevelSystemEnum.HUAN_KAO.value,
    FiveLevelSystemEnum.QUE_KAO.value: FiveLevelSystemEnum.QUE_KAO.value,
    FiveLevelSystemEnum.QU_XIAO_ZI_GE.value: FiveLevelSystemEnum.QU_XIAO_ZI_GE.value
}

TWO_LEVEL_MAP = {
    TwoLevelSystemEnum.HE_GE.value: TwoLevelSystemEnum.HE_GE.value,
    TwoLevelSystemEnum.BU_HE_GE.value: TwoLevelSystemEnum.BU_HE_GE.value,
    TwoLevelSystemEnum.MIAN_XIU.value: TwoLevelSystemEnum.MIAN_XIU.value,
    TwoLevelSystemEnum.HUAN_KAO.value: TwoLevelSystemEnum.HUAN_KAO.value,
    TwoLevelSystemEnum.QUE_KAO.value: TwoLevelSystemEnum.QUE_KAO.value,
    TwoLevelSystemEnum.QU_XIAO_ZI_GE.value: TwoLevelSystemEnum.QU_XIAO_ZI_GE.value
}
