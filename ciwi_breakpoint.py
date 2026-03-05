from control import Execute, Evaluate
from instruction import instruction
from iterators import Parallel
from measurement import BatchMeasurements
from decorator import fedt_experiment
from lib import *


def summarize(data):
    return "Material breakpoint test complete! Results saved to CSV."


@fedt_experiment
def simple_material_breakpoint_test():
    """
    Simple experiment to test breaking points of different materials.
    Uses a pre-made rectangle SVG and tests 3 materials: wood, acrylic, cardboard.
    
    Block structure:
    1. Create data collection (breakage_points)
    2. Load geometry file (rectangle.svg)
    3. Iterate over materials (Parallel)
       - Laser fabricate
       - Manual instructions
       - Measure weight at break
    4. Export data to CSV
    """
    
    # Create data collection
    breakage_points = BatchMeasurements.empty()
    
    # Load pre-made geometry file
    # Note: Create a simple rectangle SVG file or use an existing one
    rectangle_svg = GeometryFile("models/rectangle.svg")
    
    # Iterate over materials in parallel
    for material in Parallel(['wood', 'acrylic', 'cardboard']):
        # Fabricate with laser
        fabbed_object = Laser.fab(rectangle_svg, 
                                  material=material,
                                  thickness='3mm',
                                  cut_power=80,
                                  cut_speed=100)
        
        # Manual instructions for testing
        instruction("Place the object with 1cm overlapping a shelf "
                   "at each end and the remainder suspended")
        instruction("Place weights on the object until it breaks")
        
        # Measure breaking point
        breakage_points += Scale.measure_weight(fabbed_object,
                                               "total weight placed at break")
    
    # Export results
    summarize(breakage_points.get_all_data())


if __name__ == "__main__":
    # Generate flowchart (default mode)
    # from flowchart_render import render_flowchart
    # render_flowchart(simple_material_breakpoint_test)
    
    # To run actual experiment, uncomment below:
    import control
    control.MODE = Execute()
    simple_material_breakpoint_test()
