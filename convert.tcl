#   md_format_converter.convert.tcl
#
#   Copyright (C) 2012-2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
################################# PROCEDURES ##################################
proc usage {} {
    puts "usage: vmd -dispdev text -e convert.tcl -args ARGUMENTS"
}

proc help {} {
    usage
}

proc convert { inputs outputs } {

    foreach input $inputs {

        # Set defaults
        set fields [split $input :]
        set format pdb
        set first  0
        set last  -1
        set step   1

        # Parse settings
        foreach field $fields {
            set key_value [split $field =]
            set key       [lindex $key_value 0]
            set value     [lindex $key_value 1]
            puts "$key $value"
            set $key $value
        }
        if [expr ! [info exists filename]] {
            puts "ERROR: '-input' argument must include filename"
        }
        puts "FILENAME  = $filename"
        puts "FORMAT    = $format"
        puts "FIRST     = $first"
        puts "LAST      = $last"
        puts "STEP      = $step"
        
        # Load infile
        if [expr ! [info exists topology_read]] {
            mol new $filename type $format first $first last $last step $step waitfor all
            set topology_read true
        } else {
            mol addfile $filename type $format first $first last $last step $step waitfor all 0
        }

        # Delete all frames if specified (useful for loading topology)
        if {$first == -1 && $last == -1} {
            animate delete all 0
        }

        set nframes [molinfo 0 get numframes]
        puts "N_FRAMES  = $nframes"
    }

    foreach output $outputs {

        # Set defaults
        set fields [split $output :]
        set format pdb
        set selection all
        set first  0
        set last  -1
        set step   1

        # Parse setings
        foreach field $fields {
            set key_value [split $field =]
            set key       [lindex $key_value 0]
            set value     [lindex $key_value 1]
            puts "$key $value"
            set $key $value
        }
        if [expr ! [info exists filename]] {
            puts "ERROR: '-output' argument must include filename"
        }
        set selection [regsub -all {_} $selection " "]

        set nframes [molinfo 0 get numframes]
        puts "FILENAME  = $filename"
        puts "FORMAT    = $format"
        puts "SELECTION = $selection"
        puts "FIRST     = $first"
        puts "LAST      = $last"
        puts "STEP      = $step"
        puts "N_FRAMES  = $nframes"
        set selection [atomselect 0 $selection]
        puts "animate write $format $filename sel $selection beg $first end $last step $step 0 waitfor all 0"
        animate write $format $filename sel $selection beg $first end $last skip $step waitfor all 0
    }
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
#################################### MAIN #####################################
set inputs [list]
set outputs [list]
while {[llength $argv] > 0} {
    set arg [lindex $argv 0]
    set argv [lrange $argv 1 end]
    if {($arg == "-h") || ($arg == "--help")} {
        help
        exit
    } elseif {$arg == "-input"} {
        set mode "input"
    } elseif {$arg == "-output"} {
        set mode "output"
    } elseif {$mode == "input"} {
        lappend inputs $arg
    } elseif {$mode == "output"} {
        lappend outputs $arg
    } else {
        usage
    }
}
convert $inputs $outputs
exit
