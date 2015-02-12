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
    puts ""
    puts "optional arguments:"
    puts "  -h, --help            show this help message and exit"
    puts "  -d, --debug           Enable debug output"
    puts ""
    puts "input:"
    puts "  -input INPUTSPEC      Input file and settings, may be specified multiple"
    puts "                        times. Settings are provided in the format"
    puts "                        setting_1=value_1:setting_2=value_2:setting_3=value_3."
    puts "                        Supported settings are:"
    puts "                          filename: path to input file"
    puts "                          format: format of input file"
    puts "                          first: first frame to read"
    puts "                          last: last frame to read"
    puts "                          step: interval between frames"
    puts ""
    puts "output:"
    puts "  -output OUTPUTSPEC    Output file and settings, may be specified multiple"
    puts "                        times. Settings are provided in the format"
    puts "                        setting_1=value_1:setting_2=value_2:setting_3=value_3."
    puts "                        Supported settings are:"
    puts "                          filename: path to input file"
    puts "                          format: format of input file"
    puts "                          selection: atom selection to output; '_' are"
    puts "                            replaced with ' '"
    puts "                          first: first frame to read"
    puts "                          last: last frame to read"
    puts "                          step: interval between frames"
    puts "                        If first and last are both -1, only the topology will"
    puts "                        be read and all coordinates will be discarded."
}

proc convert { inputs outputs debug } {

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
            exit
        }
        if $debug {
            puts "DEBUG: filename  = $filename"
            puts "DEBUG: format    = $format"
            puts "DEBUG: first     = $first"
            puts "DEBUG: last      = $last"
            puts "DEBUG: step      = $step"
        }
        
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

        if $debug {
            set nframes [molinfo 0 get numframes]
            puts "DEBUG: n_frames  = $nframes"
        }
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
            exit
        }
        set selection [regsub -all {_} $selection " "]

        if $debug {
            set nframes [molinfo 0 get numframes]
            puts "FILENAME  = $filename"
            puts "FORMAT    = $format"
            puts "SELECTION = $selection"
            puts "FIRST     = $first"
            puts "LAST      = $last"
            puts "STEP      = $step"
            puts "N_FRAMES  = $nframes"
        }
        set selection [atomselect 0 $selection]
        puts "animate write $format $filename sel $selection beg $first end $last step $step 0 waitfor all 0"
        animate write $format $filename sel $selection beg $first end $last skip $step waitfor all 0
    }
}

#################################### MAIN #####################################

# Set defaults
set inputs [list]
set outputs [list]
set debug 0

# Parse arguments
while {[llength $argv] > 0} {
    set arg [lindex $argv 0]
    set argv [lrange $argv 1 end]
    if {($arg == "-h") || ($arg == "--help")} {
        help
        exit
    } elseif {($arg == "-d") || ($arg == "--debug")} {
        set debug 1
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

convert $inputs $outputs $debug
exit
