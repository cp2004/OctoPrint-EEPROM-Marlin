; Based on the response in issue 40 for testing printers with multiple extruders
@EEPROM_DEBUG
!!DEBUG:send echo:  G21    ; Units in mm (mm)
!!DEBUG:send
!!DEBUG:send echo:; Filament settings: Disabled
!!DEBUG:send echo:  M200 D1.75
!!DEBUG:send echo:  M200 T1 D1.75
!!DEBUG:send echo:  M200 D0
!!DEBUG:send echo:; Steps per unit:
!!DEBUG:send echo: M92 X80.00 Y80.00 Z400.00
!!DEBUG:send echo: M92 T0 E411.75
!!DEBUG:send echo: M92 T1 E93.45
!!DEBUG:send echo:; Maximum feedrates (units/s):
!!DEBUG:send echo:  M203 X500.00 Y500.00 Z6.00
!!DEBUG:send echo:  M203 T0 E30.00
!!DEBUG:send echo:  M203 T1 E30.00
!!DEBUG:send echo:; Maximum Acceleration (units/s2):
!!DEBUG:send echo:  M201 X3000.00 Y2000.00 Z60.00
!!DEBUG:send echo:  M201 T0 E10000.00
!!DEBUG:send echo:  M201 T1 E10000.00
!!DEBUG:send echo:; Acceleration (units/s2): P<print_accel> R<retract_accel> T<travel_accel>
!!DEBUG:send echo:  M204 P4000.00 R1500.00 T4000.00
!!DEBUG:send echo:; Advanced: B<min_segment_time_us> S<min_feedrate> T<min_travel_feedrate> X<max_x_jerk> Y<max_y_jerk> Z<max_z_jerk> E<max_e_jerk>
!!DEBUG:send echo:  M205 B20000.00 S0.00 T0.00 X20.00 Y20.00 Z0.40 E5.00
!!DEBUG:send echo:; Home offset:
!!DEBUG:send echo:  M206 X0.00 Y0.00 Z0.00
!!DEBUG:send echo:; Mesh Bed Leveling:
!!DEBUG:send echo:  M420 S0 Z0.00
!!DEBUG:send echo:; Endstop adjustment:
!!DEBUG:send echo:  M666 Z0.00
!!DEBUG:send echo:; PID settings:
!!DEBUG:send echo:  M301 P15.94 I1.17 D54.19
!!DEBUG:send echo:  M304 P60.37 I11.70 D207.71
!!DEBUG:send echo:; Linear Advance:
!!DEBUG:send echo:  M900 T0 K0.00
!!DEBUG:send   M900 T1 K0.00
!!DEBUG:send echo:; Filament load/unload lengths:
!!DEBUG:send echo:  M603 T0 L538.00 U555.00
!!DEBUG:send echo:  M603 T1 L538.00 U555.00
!!DEBUG:send echo:; Tool-changing:
!!DEBUG:send echo: Z2.00
!!DEBUG:send ok
M117 "blub"
