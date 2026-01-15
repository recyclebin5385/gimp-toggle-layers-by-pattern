# GIMP Toggle Layers by Pattern Plug-in

## Summary

A plug-in for GIMP 3 that toggles layer visibility according to patterns specified by the user.

## Installation

Place the entire folder into GIMPfs plug-in directory.

The folder name must match the script name:
`toggle-layers-by-pattern`

## Usage

Each layer visibility pattern is specified by a zero-based integer index.  
The plug-in determines layer visibility by parsing pattern indices embedded in layer names.

Append pattern index(es) to each layer name, delimited by a colon.  
To specify a range of integers instead of a single integer, concatenate the start and end indices with a hyphen.  
Multiple indices can be specified, delimited by commas.

Example:  
"Background layer:0", "Foreground layer:1,3-5"

Select **Layer -> Toggle Layers by Pattern** from the main menu to open the dialog.  
Specify a pattern index in the dialog and click **OK** to update the layer visibility.

## License

This project is licensed under the BSD 2-Clause License.  
See the LICENSE file for details.

## Copyright

Copyright (c) 2026 recyclebin5385
