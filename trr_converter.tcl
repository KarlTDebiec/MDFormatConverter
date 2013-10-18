# trr_converter.tcl
#   Converts trajectories to pdb and trr format
#   Written by Karl Debiec on 12-12-01
#   Last updated 13-10-18
########################################### MODULES, SETTINGS, AND DEFAULTS ############################################
package require pbctools
###################################################### FUNCTIONS #######################################################
proc usage {} {
    puts "\n\n\n"
    puts "usage: vmd -dispdev text -e xtc_converter.tcl -args {amber,anton,desmond,gromacs} arguments"
    puts "       arguments in form of [TOPOLOGY] TRAJECTORY SELECTION PDB_OUT TRR_OUT SELECTION PDB_OUT TRR_OUT ..."
    puts "       appropriate topology and trajectory input depends on package"
    puts "       SELECTION input expects underscores in place of spaces"
    puts "\n\n\n"
}

proc convert { argv } {
    puts $argv
    while { [llength $argv] >= 3} {
        regsub -all {_} [lindex $argv 0] " " sel
        set     pdb     [lindex $argv 1]
        set     trr     [lindex $argv 2]
        set     sel     [atomselect top $sel]
        animate write   pdb $pdb beg 0 end  0 sel $sel 0
        animate write   trr $trr beg 0 end -1 sel $sel 0
        set     argv    [lrange $argv 3 end]
    }
}
proc convert_amber { argv } {
    set     top     [lindex $argv 0]
    set     crd     [lindex $argv 1]
    set     type    [lindex $argv 2]
    set     argv    [lrange $argv 3 end]
    mol     new     $top type parm7     waitfor all
    mol     addfile $crd type $type     waitfor all 0
    convert $argv
}
proc convert_anton { argv } {
    set     cms     [lindex $argv 0]
    set     atr     [lindex $argv 1]
    set     argv    [lrange $argv 2 end]
    mol     new     $cms type mae   waitfor all
    mol     addfile $atr type dtr   waitfor all 0
    animate delete  beg 0 end 0 0
    convert $argv
}
proc convert_desmond { argv } {
    set     cms     [lindex $argv 0]
    set     dtr     [lindex $argv 1]
    set     argv    [lrange $argv 2 end]
    mol     new     $cms type mae   waitfor all
    mol     addfile $dtr type dtr   waitfor all 0
    animate delete  beg 0 end 1 0
    convert $argv
}
proc convert_gromacs { argv } {
    set     gro     [lindex $argv 0]
    set     xtc     [lindex $argv 1]
    set     argv    [lrange $argv 2 end]
    mol     new     $gro type gro   waitfor all
    mol     addfile $xtc type xtc   waitfor all 0
    animate delete  beg 0 end 1 0
    convert $argv
}

######################################################### MAIN #########################################################
puts $argv
if { $argc > 2 } {
    set package [string tolower [lindex $argv 0]]
    if     { $package == "amber"   } { convert_amber   [lrange $argv 1 end] } \
    elseif { $package == "anton"   } { convert_anton   [lrange $argv 1 end] } \
    elseif { $package == "desmond" } { convert_desmond [lrange $argv 1 end] } \
    elseif { $package == "gromacs" } { convert_gromacs [lrange $argv 1 end] } \
    else                             { usage }
}   else                             { usage }
exit

