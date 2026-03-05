"""
FEDT Experiment Template
========================
Use this template to create new FEDT experiments.
Key components are marked with comments.
"""

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


# REQUIRED: Summarize function (called at end of experiment)
def summarize(data):
    """
    Called at the end of the experiment to print results.
    Can return a string with analysis summary.
    """
    return "Experiment analysis complete!"


# REQUIRED: @fedt_experiment decorator
@fedt_experiment
def my_simple_experiment():
    """
    DOCSTRING: Describe what your experiment does
    - What are you testing?
    - What materials/devices do you use?
    - What do you measure?
    """
    
    
    # 1. CREATE GEOMETRY (if needed)
    
    # Create a simple shape using StlEditor
    # Format: StlEditor.cube((length, width, height))
    sample_geometry = StlEditor.cube((100, 50, 10))  # 100mm x 50mm x 10mm
    
    
    
    # 2. INITIALIZE MEASUREMENTS (where results go)
    
    # BatchMeasurements: Collects multiple measurements (most common)
    results = BatchMeasurements.empty()
    
    # Optional: ImmediateMeasurements for one-off measurements (like photos)
    photos = ImmediateMeasurements.empty()
    
    
    
    # 3. DEFINE EXPERIMENT VARIABLES (what you're testing)
    
    # These are the parameters that vary in your experiment
    material_types = ['material_A', 'material_B']
    temperatures = [20, 40, 60]  # in Celsius
    durations = [30, 60, 120]     # in seconds
    
    
    
    # 4. NESTED LOOPS (Parallel for concurrency, Series for sequence)
    
    # OUTER LOOP: Test different material types
    for material in Parallel(material_types):
        
        # MIDDLE LOOP: Test different temperatures
        for temp in Parallel(temperatures):
            
            # INNER LOOP: Sequential steps (if needed)
            for duration in Series(durations):
                
                # 5. FABRICATION (use appropriate device)

                # Device options: Printer, Laser, KnittingMachine, etc.
                instruction(f"Load {material} material")
                
                # Printer.fab() - 3D printing
                fabbed_object = Printer.fab(
                    sample_geometry,
                    material=material,
                    temperature=temp,
                    duration=duration,
                    infill_density=20
                )
                
                # Alternative: Laser.cut() for laser cutting
                # fabbed_object = Laser.cut(sample_geometry, power=100, speed=50)
                
                # Alternative: Human.post_process() for manual steps
                # fabbed_object = Human.post_process(fabbed_object, "sand and polish")
                
                
                # 6. DOCUMENTATION (optional but recommended)

                instruction("Allow material to cool/dry")
                
                # Take a photo for records
                photos += Camera.take_picture(fabbed_object, "final_sample")
                
                
                # 7. MEASUREMENT (collect data)

                # Measurement options: Protractor, Calipers, Scale, Camera, etc.
                
                # Measure a dimension
                results += Calipers.measure_size(fabbed_object, "length_mm")
                
                # Measure an angle
                results += Protractor.measure_angle(fabbed_object, "angle_degrees")
                
                # Measure weight
                results += Scale.measure_weight(fabbed_object, "weight_grams")
                
                # Alternative measurements:
                # results += Stopwatch.measure_time(fabbed_object, "processing_time_seconds")
                # results += Anemometer.measure_airflow(fabbed_object, "airspeed_mps")
    
    
    
    # 8. FINALIZE (done with experiment)
    
    # Print or process results
    summarize(results.get_all_data())



# OPTIONAL: Additional experiment variations

@fedt_experiment
def another_experiment():
    """
    You can define multiple @fedt_experiment functions in one file.
    Each will generate its own flowchart.
    """
    sample = StlEditor.cube((50, 50, 50))
    measurements = BatchMeasurements.empty()
    
    for color in Parallel(['red', 'blue', 'green']):
        instruction(f"Load {color} material")
        obj = Printer.fab(sample, color=color)
        measurements += Calipers.measure_size(obj, "size_mm")
      
    summarize(measurements.get_all_data())



# REQUIRED: Main block (generates flowchart)

if __name__ == "__main__":
    # Render flowchart for each experiment
    print("Generating flowchart for my_simple_experiment...")
    render_flowchart(my_simple_experiment)
    
    print("Generating flowchart for another_experiment...")
    render_flowchart(another_experiment)
    
    
    # OPTIONAL: To actually RUN the experiment (not just generate flowchart)
    # Uncomment the lines below:
    
    # from control import MODE, Execute
    # control.MODE = Execute()
    # my_simple_experiment()
    # another_experiment()
    
    
    # NOTE: In Execute mode, you need:
    # - Actual hardware connected (3D printer, laser, etc.)
    # - Materials loaded
    # - Measurement tools ready
    



# QUICK REFERENCE: Available Devices

# - Printer.fab()           : 3D printing (FDM)
# - Laser.cut()             : Laser cutting/engraving
# - KnittingMachine.knit()  : Knitting
# - Loom.weave()            : Weaving
# - Human.post_process()    : Manual steps
#
# Available Measurements:
# - Calipers.measure_size()      : Linear dimensions
# - Scale.measure_weight()       : Weight
# - Protractor.measure_angle()   : Angles
# - Camera.take_picture()        : Photos
# - Stopwatch.measure_time()     : Duration
# - Multimeter.measure_voltage() : Electrical
# - Anemometer.measure_airflow() : Airflow
# - Thermometer.measure_temp()   : Temperature
#
# Available Iterators:
# - Parallel([...])   : Run conditions in parallel (concurrently possible)
# - Series([...])     : Run conditions sequentially (one after another)
