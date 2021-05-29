@EEPROM_DEBUG
!!DEBUG: send echo:  G21    ; Units in mm (mm)
!!DEBUG: send echo:  M149 C ; Units in Celsius
!!DEBUG: send
!!DEBUG: send echo:; Filament settings: Disabled
!!DEBUG: send echo:  M200 S0 D1.75
!!DEBUG: send echo:; Steps per unit:
!!DEBUG: send echo: M92 X80.00 Y80.28 Z396.03 E98.41
!!DEBUG: send echo:; Maximum feedrates (units/s):
!!DEBUG: send echo:  M203 X500.00 Y500.00 Z10.00 E60.00
!!DEBUG: send echo:; Maximum Acceleration (units/s2):
!!DEBUG: send echo:  M201 X500.00 Y500.00 Z100.00 E5000.00
!!DEBUG: send echo:; Acceleration (units/s2): P<print_accel> R<retract_accel> T<travel_accel>
!!DEBUG: send echo:  M204 P500.00 R1000.00 T500.00
!!DEBUG: send echo:; Advanced: B<min_segment_time_us> S<min_feedrate> T<min_travel_feedrate> J<junc_dev>
!!DEBUG: send echo:  M205 B20000.00 S0.00 T0.00 J0.08
!!DEBUG: send echo:; Home offset:
!!DEBUG: send echo:  M206 X0.00 Y0.00 Z0.00
!!DEBUG: send echo:; Auto Bed Leveling:
!!DEBUG: send echo:  M420 S0 Z10.00
!!DEBUG: send echo:  G29 W I0 J0 Z-0.51000
!!DEBUG: send echo:  G29 W I1 J0 Z-0.54750
!!DEBUG: send echo:  G29 W I2 J0 Z-0.53000
!!DEBUG: send echo:  G29 W I3 J0 Z-0.53250
!!DEBUG: send echo:  G29 W I4 J0 Z-0.56000
!!DEBUG: send echo:  G29 W I0 J1 Z-0.57250
!!DEBUG: send echo:  G29 W I1 J1 Z-0.61000
!!DEBUG: send echo:  G29 W I2 J1 Z-0.59000
!!DEBUG: send echo:  G29 W I3 J1 Z-0.60750
!!DEBUG: send echo:  G29 W I4 J1 Z-0.64250
!!DEBUG: send echo:  G29 W I0 J2 Z-0.59500
!!DEBUG: send echo:  G29 W I1 J2 Z-0.61750
!!DEBUG: send echo:  G29 W I2 J2 Z-0.60250
!!DEBUG: send echo:  G29 W I3 J2 Z-0.62750
!!DEBUG: send echo:  G29 W I4 J2 Z-0.65500
!!DEBUG: send echo:  G29 W I0 J3 Z-0.58750
!!DEBUG: send echo:  G29 W I1 J3 Z-0.62500
!!DEBUG: send echo:  G29 W I2 J3 Z-0.61750
!!DEBUG: send echo:  G29 W I3 J3 Z-0.63000
!!DEBUG: send echo:  G29 W I4 J3 Z-0.64250
!!DEBUG: send echo:  G29 W I0 J4 Z-0.54500
!!DEBUG: send echo:  G29 W I1 J4 Z-0.60500
!!DEBUG: send echo:  G29 W I2 J4 Z-0.60250
!!DEBUG: send echo:  G29 W I3 J4 Z-0.61750
!!DEBUG: send echo:  G29 W I4 J4 Z-0.64000
!!DEBUG: send echo:; Material heatup parameters:
!!DEBUG: send echo:  M145 S0 H185.00 B45.00 F255
!!DEBUG: send echo:  M145 S1 H240.00 B110.00 F255
!!DEBUG: send echo:; PID settings:
!!DEBUG: send echo:  M301 P28.72 I2.82 D73.10
!!DEBUG: send echo:  M304 P92.30 I17.71 D320.68
!!DEBUG: send ; Controller Fan
!!DEBUG: send echo:  M710 S255 I0 A1 D60 ; (100% 0%)
!!DEBUG: send echo:; Power-Loss Recovery:
!!DEBUG: send echo:  M413 S1
!!DEBUG: send echo:; Z-Probe Offset (mm):
!!DEBUG: send echo:  M851 X-39.80 Y-8.50 Z-1.71
!!DEBUG: send echo:; Stepper driver current:
!!DEBUG: send echo:  M906 X580 Y580 Z580
!!DEBUG: send echo:  M906 T0 E650
!!DEBUG: send
!!DEBUG: send echo:; Driver stepping mode:
!!DEBUG: send echo:  M569 S1 X Y Z
!!DEBUG: send echo:  M569 S1 T0 E
!!DEBUG: send echo:; Filament load/unload lengths:
!!DEBUG: send echo:  M603 L350.00 U400.00
!!DEBUG: send ok
