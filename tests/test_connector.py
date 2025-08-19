import math

from octopus_exercise.etl.transform import ConnectorETLModel, PowerTypeEnum


def test_single_phase_conversion_without_max_electric_power():
    model = ConnectorETLModel(
        power_type=PowerTypeEnum.AC_1_PHASE.name,
        max_amperage=16,
        max_voltage=230
    )
    
    expected = round(16 * 230 / 1000) * 1000
    assert model.max_electric_power == expected

def test_three_phase_conversion():
    model = ConnectorETLModel(
        power_type=PowerTypeEnum.AC_3_PHASE.name,
        max_amperage=32,
        max_voltage=400
    )
    
    expected = round(math.sqrt(3) * 400 * 32 / 1000) * 1000
    assert model.max_electric_power == expected

def test_max_electric_power_preserved():
    # If max_electric_power is already set, it should not calculate it again
    model = ConnectorETLModel(
        power_type=PowerTypeEnum.AC_3_PHASE.name,
        max_amperage=32,
        max_voltage=400,
        max_electric_power=99999
    )
    
    assert model.max_electric_power == 99999
