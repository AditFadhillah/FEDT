from numpy import arange

import control
from control import Execute, Evaluate
from instruction import instruction
from iterators import Parallel, Series, shuffle, include_last
from measurement import BatchMeasurements, ImmediateMeasurements
from flowchart import FlowChart
from flowchart_render import render_flowchart
from decorator import fedt_experiment
from lib import *


def summarize(data):
    return "4D printing shape-change analysis complete!"


@fedt_experiment
def test_material_type_inconsistency():
    """
    REPLICATES UIT PAPER FINDINGS (Section 4.2 Limitations)
    
    The paper found that despite using "identical filaments", different colors
    of PLA Basic (same material type) bent inconsistently:
    - Gold, bronze-green, pink, light gray should have identical properties
    - But they all bent differently
    - PLA-CF (carbon-fiber) was stiffer than PLA Basic
    - But purple PLA-CF bent differently than expected
    
    This experiment tests this exact inconsistency:
    - PLA Basic vs PLA-CF material types (Bambu Lab filaments)
    - Multiple colors within each material type
    - Controlled single-dip protocol for consistency
    """
    
    plate_template = StlEditor.cube((80, 40, 2))
    bend_measurements = BatchMeasurements.empty()
    
    # PLA Basic colors (should have same properties but don't according to paper)
    pla_basic_colors = ['Gold', 'Bronze_Green', 'Pink', 'Light_Gray', 'Natural']
    # PLA-CF colors (carbon-fiber reinforced, stiffer)
    pla_cf_colors = ['Black', 'Purple']
    
    # Test PLA Basic first
    for color in Parallel(pla_basic_colors):
        instruction(f"Load PLA_Basic filament: {color}")
        fabbed_object = Printer.fab(plate_template,
                                   material='PLA_Basic',
                                   filament_color=color,
                                   infill_density=20,
                                   layer_height='0.2mm')
        
        instruction("Cool to room temperature")
        instruction("Place in 80°C water bath for 30 seconds")
        
        fabbed_object = Human.post_process(fabbed_object,
                                          f"heat-activate and cool in bent configuration")
        
        # Measure bending angle
        bend_measurements += Protractor.measure_angle(fabbed_object,
                                                     "bend_angle_degrees")
        bend_measurements += Calipers.measure_size(fabbed_object,
                                                  "tip_displacement_mm")
    
    # Test PLA-CF (should be stiffer)
    for color in Parallel(pla_cf_colors):
        instruction(f"Load PLA_CF filament: {color}")
        fabbed_object = Printer.fab(plate_template,
                                   material='PLA_CF',
                                   filament_color=color,
                                   infill_density=20,
                                   layer_height='0.2mm')
        
        instruction("Cool to room temperature")
        instruction("Place in 80°C water bath for 30 seconds")
        
        fabbed_object = Human.post_process(fabbed_object,
                                          f"heat-activate and cool in bent configuration")
        
        bend_measurements += Protractor.measure_angle(fabbed_object,
                                                     "bend_angle_degrees")
        bend_measurements += Calipers.measure_size(fabbed_object,
                                                  "tip_displacement_mm")
    
    # Output reveals which colors/materials bent unexpectedly
    summarize(bend_measurements.get_all_data())


if __name__ == "__main__":
    # Create flowchart (Evaluate mode - default)
    print("Generating flowchart for material type inconsistency test (Section 4.2 Limitations)...")
    render_flowchart(test_material_type_inconsistency)
    
    # Uncomment below to run actual experiment (Execute mode)
    # This would require actual 3D printer and measurement equipment
    # from control import MODE, Execute
    # control.MODE = Execute()
    # test_material_type_inconsistency()
