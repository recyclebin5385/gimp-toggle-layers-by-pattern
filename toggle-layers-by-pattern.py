#!/usr/bin/env python3

# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2026 recyclebin5385

import gi
gi.require_version('Gimp', '3.0')
gi.require_version('GimpUi', '3.0')
from gi.repository import Gimp, GObject, GLib, GimpUi
import sys
import re

NAME_INDEXES_PATTERN = r":\s*((?:[0-9]+\s*(?:-\s*(?:[0-9]+)?)?)(?:,\s*(?:[0-9]+\s*(?:-\s*(?:[0-9]+)?)?))*)"
NAME_INDEX_RANGE_PATTERN = r"([0-9]+)\s*(?:(-)\s*([0-9]+)?)?"

plug_in_binary = "toggle-layers-by-pattern"
plug_in_proc = "plug-in-recyclebin5385-" + plug_in_binary

class ToggleLayersByPattern(Gimp.PlugIn):
    def do_query_procedures(self):
        return [ plug_in_proc ]

    def do_create_procedure(self, name):
        proc = None

        if name == plug_in_proc:
            proc = Gimp.ImageProcedure.new(
                self,
                name,
                Gimp.PDBProcType.PLUGIN,
                self.run,
                None
            )

            proc.set_menu_label("_Toggle Layers by Pattern")
            proc.add_menu_path("<Image>/Layer")
            proc.set_attribution("recyclebin5385", "recyclebin5385", "2026")
            proc.set_image_types("*")
            proc.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.DRAWABLE | Gimp.ProcedureSensitivityMask.NO_DRAWABLES)

            proc.add_int_argument(
                "index",
                "Pattern index",
                None,
                0, # min
                99, # max
                0, # default
                GObject.ParamFlags.READWRITE
            )

        return proc

    def run(self, procedure, run_mode, image, drawables, config, data):
        if run_mode == Gimp.RunMode.INTERACTIVE:
            GimpUi.init(plug_in_binary)

            dialog = GimpUi.ProcedureDialog.new(procedure, config, "Toggle Layers by Pattern")
            dialog.fill(["index"])
            if not dialog.run():
                dialog.destroy()
                return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, None)
            else:
                dialog.destroy()

        index = config.get_property("index")

        image.undo_group_start()
        try:
            for i, layer in enumerate(iter_layers(image)):
                ranges = extract_index_ranges_from_name(layer.get_name())
                if ranges is not None:
                    layer.set_visible(ranges_includes(ranges, index))
        finally:
            image.undo_group_end()

        Gimp.displays_flush()

        return procedure.new_return_values(
            Gimp.PDBStatusType.SUCCESS,
            GLib.Error()
        )

def iter_layers(parent, depth=0):
    for layer in parent.get_layers() if isinstance(parent, Gimp.Image) else parent.get_children():
        yield layer
        yield from iter_layers(layer, depth + 1)

def extract_index_ranges_from_name(name):
    m = re.search(NAME_INDEXES_PATTERN, name)
    if not m:
        return None
    ret = []
    for x in re.findall(NAME_INDEX_RANGE_PATTERN, m.group(1)):
        if x[1]:
            if x[2]:
                r = [int(x[0]), int(x[2])]
            else:
                r = [int(x[0]), None]
        else:
            r = [int(x[0]), int(x[0])]
        ret.append(r)
    return ret

def ranges_includes(ranges, x):
    for r in ranges:
        if r[0] <= x and (r[1] is None or x <= r[1]):
            return True
    return False

Gimp.main(ToggleLayersByPattern.__gtype__, sys.argv)
