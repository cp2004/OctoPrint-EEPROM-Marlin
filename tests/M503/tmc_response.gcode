; @MMcLure
@EEPROM_DEBUG ; trigger data collection
!!DEBUG: send echo:  G21    ; Units in mm (mm)
!!DEBUG: send echo:  M149 C ; Units in Celsius
!!DEBUG: send
!!DEBUG: send echo:; Filament settings: Disabled
!!DEBUG: send echo:  M200 S0 D1.7500
!!DEBUG: send echo:; Steps per unit:
!!DEBUG: send echo: M92 X200.0000 Y200.0000 Z400.0000 E415.0000
!!DEBUG: send echo:; Maximum feedrates (units/s):
!!DEBUG: send echo:  M203 X400.0000 Y400.0000 Z8.0000 E50.0000
!!DEBUG: send echo:; Maximum Acceleration (units/s2):
!!DEBUG: send echo:  M201 X2000.0000 Y2000.0000 Z100.0000 E10000.0000
!!DEBUG: send echo:; Acceleration (units/s2): P<print_accel> R<retract_accel> T<travel_accel>
!!DEBUG: send echo:  M204 P800.0000 R10000.0000 T2000.0000
!!DEBUG: send echo:; Advanced: B<min_segment_time_us> S<min_feedrate> T<min_travel_feedrate> X<max_x_jerk> Y<max_y_jerk> Z<max_z_jerk> E<max_e_jerk>
!!DEBUG: send echo:  M205 B20000.0000 S0.0000 T0.0000 X8.0000 Y8.0000 Z0.3000 E5.0000
!!DEBUG: send echo:; Home offset:
!!DEBUG: send echo:  M206 X0.0000 Y0.0000 Z0.0000
!!DEBUG: send echo:; Unified Bed Leveling:
!!DEBUG: send echo:  M420 S1 Z10.0000
!!DEBUG: send
!!DEBUG: send Unified Bed Leveling System v1.01 active
!!DEBUG: send
!!DEBUG: send echo:; Active Mesh Slot: 0
!!DEBUG: send echo:; EEPROM can hold 3 meshes.
!!DEBUG: send
!!DEBUG: send echo:; Material heatup parameters:
!!DEBUG: send echo:  M145 S0 H190.0000 B60.0000 F0
!!DEBUG: send echo:  M145 S1 H210.0000 B70.0000 F0
!!DEBUG: send echo:; PID settings:
!!DEBUG: send echo:  M301 P19.0986 I1.3998 D65.1453
!!DEBUG: send echo:  M304 P46.3000 I9.0700 D157.5700
!!DEBUG: send echo:; Z-Probe Offset (mm):
!!DEBUG: send echo:  M851 X-29.0000 Y1.0000 Z-1.9250
!!DEBUG: send echo:; Stepper driver current:
!!DEBUG: send echo:  M906 X1200 Y1200 Z400
!!DEBUG: send echo:  M906 I1 Z400
!!DEBUG: send echo:  M906 T0 E900
!!DEBUG: send
!!DEBUG: send echo:; Driver stepping mode:
!!DEBUG: send echo:  M569 S1 X Y Z
!!DEBUG: send echo:  M569 S1 I1 Z
!!DEBUG: send echo:; Linear Advance:
!!DEBUG: send echo:  M900 K0.0400
!!DEBUG: send echo:; Filament load/unload lengths:
!!DEBUG: send echo:  M603 L25.0000 U75.0000
!!DEBUG: send echo:; Filament runout sensor:
!!DEBUG: send echo:  M412 S0
!!DEBUG: send ok P63 B31
