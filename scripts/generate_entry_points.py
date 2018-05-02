#!/usr/bin/python2
#
# Copyright 2017 The ANGLE Project Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# generate_entry_points.py:
#   Generates the OpenGL bindings and entry point layers for ANGLE.

import sys, os, pprint, json
import xml.etree.ElementTree as etree
from datetime import date

# List of supported extensions. Add to this list to enable new extensions
# available in gl.xml.

angle_extensions = [
    # ANGLE extensions
    "GL_CHROMIUM_bind_uniform_location",
    "GL_CHROMIUM_framebuffer_mixed_samples",
    "GL_CHROMIUM_path_rendering",
    "GL_CHROMIUM_copy_texture",
    "GL_CHROMIUM_copy_compressed_texture",
    "GL_ANGLE_request_extension",
    "GL_ANGLE_robust_client_memory",
    "GL_ANGLE_multiview",
]

gles1_extensions = [
    # ES1 (Possibly the min set of extensions needed by Android)
    "GL_OES_draw_texture",
    "GL_OES_framebuffer_object",
    "GL_OES_matrix_palette",
    "GL_OES_point_size_array",
    "GL_OES_query_matrix",
    "GL_OES_texture_cube_map",
]

# List of GLES1 extensions for which we don't need to add Context.h decls.
gles1_no_context_decl_extensions = [
    "GL_OES_framebuffer_object",
]

# List of GLES1 API calls that have had their semantics changed in later GLES versions, but the
# name was kept the same
gles1_overloaded = [
    "glGetPointerv",
]

supported_extensions = sorted(angle_extensions + gles1_extensions + [
    # ES2+
    "GL_ANGLE_framebuffer_blit",
    "GL_ANGLE_framebuffer_multisample",
    "GL_ANGLE_instanced_arrays",
    "GL_ANGLE_translated_shader_source",
    "GL_EXT_debug_marker",
    "GL_EXT_discard_framebuffer",
    "GL_EXT_disjoint_timer_query",
    "GL_EXT_draw_buffers",
    "GL_EXT_map_buffer_range",
    "GL_EXT_occlusion_query_boolean",
    "GL_EXT_robustness",
    "GL_EXT_texture_storage",
    "GL_KHR_debug",
    "GL_NV_fence",
    "GL_OES_EGL_image",
    "GL_OES_get_program_binary",
    "GL_OES_mapbuffer",
    "GL_OES_vertex_array_object",
])

# The EGL_ANGLE_explicit_context extension is generated differently from other extensions.
# Toggle generation here.
support_EGL_ANGLE_explicit_context = True

# This is a list of exceptions for entry points which don't want to have
# the EVENT macro. This is required for some debug marker entry points.
no_event_marker_exceptions_list = sorted([
    "glPushGroupMarkerEXT",
    "glPopGroupMarkerEXT",
    "glInsertEventMarkerEXT",
])

# Strip these suffixes from Context entry point names. NV is excluded (for now).
strip_suffixes = ["ANGLE", "EXT", "KHR", "OES", "CHROMIUM"]

template_entry_point_header = """// GENERATED FILE - DO NOT EDIT.
// Generated by {script_name} using data from {data_source_name}.
//
// Copyright {year} The ANGLE Project Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// entry_points_gles_{annotation_lower}_autogen.h:
//   Defines the GLES {comment} entry points.

#ifndef LIBGLESV2_ENTRY_POINTS_GLES_{annotation_upper}_AUTOGEN_H_
#define LIBGLESV2_ENTRY_POINTS_GLES_{annotation_upper}_AUTOGEN_H_

{includes}

namespace gl
{{
{entry_points}
}}  // namespace gl

#endif  // LIBGLESV2_ENTRY_POINTS_GLES_{annotation_upper}_AUTOGEN_H_
"""

template_entry_point_source = """// GENERATED FILE - DO NOT EDIT.
// Generated by {script_name} using data from {data_source_name}.
//
// Copyright {year} The ANGLE Project Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// entry_points_gles_{annotation_lower}_autogen.cpp:
//   Defines the GLES {comment} entry points.

{includes}

namespace gl
{{
{entry_points}}}  // namespace gl
"""

template_entry_points_enum_header = """// GENERATED FILE - DO NOT EDIT.
// Generated by {script_name} using data from {data_source_name}.
//
// Copyright {year} The ANGLE Project Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// entry_points_enum_autogen.h:
//   Defines the GLES entry points enumeration.

#ifndef LIBGLESV2_ENTRYPOINTSENUM_AUTOGEN_H_
#define LIBGLESV2_ENTRYPOINTSENUM_AUTOGEN_H_

namespace gl
{{
enum class EntryPoint
{{
{entry_points_list}
}};
}}  // namespace gl
#endif  // LIBGLESV2_ENTRY_POINTS_ENUM_AUTOGEN_H_
"""

template_libgles_entry_point_source = """// GENERATED FILE - DO NOT EDIT.
// Generated by {script_name} using data from {data_source_name}.
//
// Copyright {year} The ANGLE Project Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// libGLESv2.cpp: Implements the exported OpenGL ES functions.

{includes}
extern "C" {{
{entry_points}
}} // extern "C"
"""

template_libgles_entry_point_export = """; GENERATED FILE - DO NOT EDIT.
; Generated by {script_name} using data from {data_source_name}.
;
; Copyright {year} The ANGLE Project Authors. All rights reserved.
; Use of this source code is governed by a BSD-style license that can be
; found in the LICENSE file.
LIBRARY libGLESv2
EXPORTS
{exports}
"""

template_entry_point_decl = """ANGLE_EXPORT {return_type}GL_APIENTRY {name}({params});"""
template_entry_point_decl = """ANGLE_EXPORT {return_type}GL_APIENTRY {name}{explicit_context_suffix}({explicit_context_param}{explicit_context_comma}{params});"""

template_entry_point_def = """{return_type}GL_APIENTRY {name}{explicit_context_suffix}({explicit_context_param}{explicit_context_comma}{params})
{{
    {event_comment}EVENT("({format_params})"{comma_if_needed}{pass_params});

    Context *context = {context_getter};
    if (context)
    {{{assert_explicit_context}{packed_gl_enum_conversions}
        context->gatherParams<EntryPoint::{name}>({internal_params});

        if (context->skipValidation() || Validate{name}({validate_params}))
        {{
            {return_if_needed}context->{name_lower_no_suffix}({internal_params});
        }}
    }}
{default_return_if_needed}}}
"""

context_gles_header = """// GENERATED FILE - DO NOT EDIT.
// Generated by {script_name} using data from {data_source_name}.
//
// Copyright {year} The ANGLE Project Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// Context_gles_{annotation_lower}_autogen.h: Creates a macro for interfaces in Context.

#ifndef ANGLE_CONTEXT_GLES_{annotation_upper}_AUTOGEN_H_
#define ANGLE_CONTEXT_GLES_{annotation_upper}_AUTOGEN_H_

#define ANGLE_GLES1_CONTEXT_API \\
{interface}

#endif // ANGLE_CONTEXT_API_{annotation_upper}_AUTOGEN_H_
"""

context_gles_decl = """    {return_type} {name_lower_no_suffix}({internal_params}); \\"""

libgles_entry_point_def = """{return_type}GL_APIENTRY gl{name}{explicit_context_suffix}({explicit_context_param}{explicit_context_comma}{params})
{{
    return gl::{name}{explicit_context_suffix}({explicit_context_internal_param}{explicit_context_comma}{internal_params});
}}
"""

libgles_entry_point_export = """    {name}{explicit_context_suffix}{spaces}@{ordinal}"""

template_glext_explicit_context_inc = """// GENERATED FILE - DO NOT EDIT.
// Generated by {script_name} using data from {data_source_name}.
//
// Copyright {year} The ANGLE Project Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// gl{version}ext_explicit_context_autogen.inc:
//   Function declarations for the EGL_ANGLE_explicit_context extension

{function_pointers}
#ifdef GL_GLEXT_PROTOTYPES
{function_prototypes}
#endif
"""

template_glext_function_pointer = """typedef {return_type}(GL_APIENTRYP PFN{name_upper}{explicit_context_suffix_upper})({explicit_context_param}{explicit_context_comma}{params});"""
template_glext_function_prototype = """{apicall} {return_type}GL_APIENTRY {name}{explicit_context_suffix}({explicit_context_param}{explicit_context_comma}{params});"""

def script_relative(path):
    return os.path.join(os.path.dirname(sys.argv[0]), path)

tree = etree.parse(script_relative('gl.xml'))
root = tree.getroot()
commands = root.find(".//commands[@namespace='GL']")

with open(script_relative('entry_point_packed_gl_enums.json')) as f:
    cmd_packed_gl_enums = json.loads(f.read())

def format_entry_point_decl(cmd_name, proto, params, is_explicit_context):
    comma_if_needed = ", " if len(params) > 0 else ""
    return template_entry_point_decl.format(
        name = cmd_name[2:],
        return_type = proto[:-len(cmd_name)],
        params = ", ".join(params),
        comma_if_needed = comma_if_needed,
        explicit_context_suffix = "ContextANGLE" if is_explicit_context else "",
        explicit_context_param = "GLeglContext ctx" if is_explicit_context else "",
        explicit_context_comma = ", " if is_explicit_context and len(params) > 0 else "")

def type_name_sep_index(param):
    space = param.rfind(" ")
    pointer = param.rfind("*")
    return max(space, pointer)

def just_the_type(param):
    if "*" in param:
        return param[:type_name_sep_index(param) + 1]
    return param[:type_name_sep_index(param)]

def just_the_name(param):
    return param[type_name_sep_index(param)+1:]

def make_param(param_type, param_name):
    return param_type + " " + param_name

def just_the_type_packed(param, entry):
    name = just_the_name(param)
    if entry.has_key(name):
        return entry[name]
    else:
        return just_the_type(param)

def just_the_name_packed(param, reserved_set):
    name = just_the_name(param)
    if name in reserved_set:
        return name + 'Packed'
    else:
        return name

format_dict = {
    "GLbitfield": "0x%X",
    "GLboolean": "%u",
    "GLclampx": "0x%X",
    "GLenum": "0x%X",
    "GLfixed": "0x%X",
    "GLfloat": "%f",
    "GLint": "%d",
    "GLintptr": "%d",
    "GLshort": "%d",
    "GLsizei": "%d",
    "GLsizeiptr": "%d",
    "GLsync": "0x%0.8p",
    "GLubyte": "%d",
    "GLuint": "%u",
    "GLuint64": "%llu",
    "GLDEBUGPROC": "0x%0.8p",
    "GLDEBUGPROCKHR": "0x%0.8p",
    "GLeglImageOES": "0x%0.8p",
}

def param_format_string(param):
    if "*" in param:
        return param + " = 0x%0.8p"
    else:
        type_only = just_the_type(param)
        if type_only not in format_dict:
            raise Exception(type_only + " is not a known type in 'format_dict'")

        return param + " = " + format_dict[type_only]

def default_return_value(cmd_name, return_type):
    if return_type == "void":
        return ""
    return "GetDefaultReturnValue<EntryPoint::" + cmd_name[2:] + ", " + return_type + ">()"

def get_context_getter_function(cmd_name, is_explicit_context):
    if cmd_name == "glGetError":
        return "GetGlobalContext()"
    elif is_explicit_context:
        return "static_cast<gl::Context *>(ctx)"
    else:
        return "GetValidGlobalContext()"

template_event_comment = """// Don't run an EVENT() macro on the EXT_debug_marker entry points.
    // It can interfere with the debug events being set by the caller.
    // """

def format_entry_point_def(cmd_name, proto, params, is_explicit_context):
    packed_gl_enums = cmd_packed_gl_enums.get(cmd_name, {})
    internal_params = [just_the_name_packed(param, packed_gl_enums) for param in params]
    packed_gl_enum_conversions = []
    for param in params:
        name = just_the_name(param)
        if name in packed_gl_enums:
            internal_name = name + "Packed"
            internal_type = packed_gl_enums[name]
            packed_gl_enum_conversions += ["\n        " + internal_type + " " + internal_name +" = FromGLenum<" +
                                          internal_type + ">(" + name + ");"]

    pass_params = [just_the_name(param) for param in params]
    format_params = [param_format_string(param) for param in params]
    return_type = proto[:-len(cmd_name)]
    default_return = default_return_value(cmd_name, return_type.strip())
    event_comment = template_event_comment if cmd_name in no_event_marker_exceptions_list else ""
    name_lower_no_suffix = cmd_name[2:3].lower() + cmd_name[3:]

    for suffix in strip_suffixes:
        if name_lower_no_suffix.endswith(suffix):
            name_lower_no_suffix = name_lower_no_suffix[0:-len(suffix)]

    return template_entry_point_def.format(
        name = cmd_name[2:],
        name_lower_no_suffix = name_lower_no_suffix,
        return_type = return_type,
        params = ", ".join(params),
        internal_params = ", ".join(internal_params),
        packed_gl_enum_conversions = "".join(packed_gl_enum_conversions),
        pass_params = ", ".join(pass_params),
        comma_if_needed = ", " if len(params) > 0 else "",
        validate_params = ", ".join(["context"] + internal_params),
        format_params = ", ".join(format_params),
        return_if_needed = "" if default_return == "" else "return ",
        default_return_if_needed = "" if default_return == "" else "\n    return " + default_return + ";\n",
        context_getter = get_context_getter_function(cmd_name, is_explicit_context),
        event_comment = event_comment,
        explicit_context_suffix = "ContextANGLE" if is_explicit_context else "",
        explicit_context_param = "GLeglContext ctx" if is_explicit_context else "",
        explicit_context_comma = ", " if is_explicit_context and len(params) > 0 else "",
        assert_explicit_context = "\nASSERT(context == GetValidGlobalContext());"
            if is_explicit_context else "")

def format_context_gles_decl(cmd_name, proto, params):
    packed_gl_enums = cmd_packed_gl_enums.get(cmd_name, {})
    internal_params = ", ".join([make_param(just_the_type_packed(param, packed_gl_enums),
                                 just_the_name_packed(param, packed_gl_enums)) for param in params])

    return_type = proto[:-len(cmd_name)]
    name_lower_no_suffix = cmd_name[2:3].lower() + cmd_name[3:]

    for suffix in strip_suffixes:
        if name_lower_no_suffix.endswith(suffix):
            name_lower_no_suffix = name_lower_no_suffix[0:-len(suffix)]

    return context_gles_decl.format(
        return_type = return_type,
        name_lower_no_suffix = name_lower_no_suffix,
        internal_params = internal_params)

def format_libgles_entry_point_def(cmd_name, proto, params, is_explicit_context):
    internal_params = [just_the_name(param) for param in params]
    return_type = proto[:-len(cmd_name)]

    return libgles_entry_point_def.format(
        name = cmd_name[2:],
        return_type = return_type,
        params = ", ".join(params),
        internal_params = ", ".join(internal_params),
        explicit_context_suffix = "ContextANGLE" if is_explicit_context else "",
        explicit_context_param = "GLeglContext ctx" if is_explicit_context else "",
        explicit_context_comma = ", " if is_explicit_context and len(params) > 0 else "",
        explicit_context_internal_param = "ctx" if is_explicit_context else "")

def format_libgles_entry_point_export(cmd_name, ordinal, is_explicit_context):
    return libgles_entry_point_export.format(
        name = cmd_name,
        ordinal = ordinal,
        spaces = " "*(50 - len(cmd_name)),
        explicit_context_suffix = "ContextANGLE" if is_explicit_context else "")

def path_to(folder, file):
    return os.path.join(script_relative(".."), "src", folder, file)

def get_entry_points(all_commands, gles_commands, ordinal, is_explicit_context):
    decls = []
    defs = []
    export_defs = []
    exports = []

    for command in all_commands:
        proto = command.find('proto')
        cmd_name = proto.find('name').text

        if cmd_name not in gles_commands:
            continue

        param_text = ["".join(param.itertext()) for param in command.findall('param')]
        proto_text = "".join(proto.itertext())
        decls.append(format_entry_point_decl(cmd_name, proto_text, param_text,
            is_explicit_context))
        defs.append(format_entry_point_def(cmd_name, proto_text, param_text, is_explicit_context))

        export_defs.append(format_libgles_entry_point_def(cmd_name, proto_text, param_text,
            is_explicit_context))
        exports.append(format_libgles_entry_point_export(cmd_name, ordinal, is_explicit_context))
        ordinal = ordinal + 1

    return decls, defs, export_defs, exports

def get_gles1_decls(all_commands, gles_commands):
    decls = []
    for command in all_commands:
        proto = command.find('proto')
        cmd_name = proto.find('name').text

        if cmd_name not in gles_commands:
            continue

        if cmd_name in gles1_overloaded:
            continue

        param_text = ["".join(param.itertext()) for param in command.findall('param')]
        proto_text = "".join(proto.itertext())
        decls.append(format_context_gles_decl(cmd_name, proto_text, param_text))

    return decls

def get_glext_decls(all_commands, gles_commands, version, is_explicit_context):
    glext_ptrs = []
    glext_protos = []
    is_gles1 = False

    if(version == ""):
        is_gles1 = True

    for command in all_commands:
        proto = command.find('proto')
        cmd_name = proto.find('name').text

        if cmd_name not in gles_commands:
            continue

        param_text = ["".join(param.itertext()) for param in command.findall('param')]
        proto_text = "".join(proto.itertext())

        return_type = proto_text[:-len(cmd_name)]
        params = ", ".join(param_text)

        format_params = {
            "apicall": "GL_API" if is_gles1 else "GL_APICALL",
            "name": cmd_name,
            "name_upper": cmd_name.upper(),
            "return_type": return_type,
            "params": params,
            "explicit_context_comma": ", " if is_explicit_context and len(params) > 0 else "",
            "explicit_context_suffix": "ContextANGLE" if is_explicit_context else "",
            "explicit_context_suffix_upper": "CONTEXTANGLE" if is_explicit_context else "",
            "explicit_context_param": "GLeglContext ctx" if is_explicit_context else ""}

        glext_ptrs.append(template_glext_function_pointer.format(
            **format_params))
        glext_protos.append(template_glext_function_prototype.format(
            **format_params))

    return glext_ptrs, glext_protos

def write_file(annotation, comment, template, entry_points, suffix, includes, file):

    content = template.format(
        script_name = os.path.basename(sys.argv[0]),
        data_source_name = file,
        year = date.today().year,
        annotation_lower = annotation.lower(),
        annotation_upper = annotation.upper(),
        comment = comment,
        includes = includes,
        entry_points = entry_points)

    path = path_to("libGLESv2", "entry_points_gles_{}_autogen.{}".format(
        annotation.lower(), suffix))

    with open(path, "w") as out:
        out.write(content)
        out.close()

def write_export_files(entry_points, includes, exports):

    content = template_libgles_entry_point_source.format(
        script_name = os.path.basename(sys.argv[0]),
        data_source_name = "gl.xml and gl_angle_ext.xml",
        year = date.today().year,
        includes = includes,
        entry_points = entry_points)

    path = path_to("libGLESv2", "libGLESv2_autogen.cpp")

    with open(path, "w") as out:
        out.write(content)
        out.close()

    content = template_libgles_entry_point_export.format(
        script_name = os.path.basename(sys.argv[0]),
        data_source_name = "gl.xml and gl_angle_ext.xml",
        exports = exports,
        year = date.today().year)

    path = path_to("libGLESv2", "libGLESv2_autogen.def")

    with open(path, "w") as out:
        out.write(content)
        out.close()

def write_context_api_decls(annotation, template, decls):

    interface_lines = []

    for i in decls['core']:
        interface_lines.append(i)

    for extname in sorted(decls['exts'].keys()):
        interface_lines.append("    /* " + extname + " */ \\")
        interface_lines.extend(decls['exts'][extname])

    content = template.format(
        annotation_lower = annotation.lower(),
        annotation_upper = annotation.upper(),
        script_name = os.path.basename(sys.argv[0]),
        data_source_name = "gl.xml",
        year = date.today().year,
        interface = "\n".join(interface_lines))

    path = path_to("libANGLE", "Context_gles_%s_autogen.h" % annotation.lower())

    with open(path, "w") as out:
        out.write(content)
        out.close()

def write_glext_explicit_context_inc(version, ptrs, protos):
    folder_version = version if version != "31" else "3"

    content = template_glext_explicit_context_inc.format(
        script_name = os.path.basename(sys.argv[0]),
        data_source_name = "gl.xml and gl_angle_ext.xml",
        year = date.today().year,
        version = version,
        function_pointers = ptrs,
        function_prototypes = protos)

    path = path_to("..\include\GLES{}".format(folder_version),
        "gl{}ext_explicit_context_autogen.inc".format(version))

    with open(path, "w") as out:
        out.write(content)
        out.close()

def append_angle_extensions(base_root):
    angle_ext_tree = etree.parse(script_relative('gl_angle_ext.xml'))
    angle_ext_root = angle_ext_tree.getroot()

    insertion_point = base_root.findall("./commands")[0]
    for command in angle_ext_root.iter('commands'):
        insertion_point.extend(command)

    insertion_point = base_root.findall("./extensions")[0]
    for extension in angle_ext_root.iter('extensions'):
        insertion_point.extend(extension)
    return base_root

class GLCommandNames:
    def __init__(self):
        self.command_names = {}

    def get_commands(self, version):
        return self.command_names[version]

    def get_all_commands(self):
        cmd_names = []
        # Combine all the version lists into a single list
        for version, version_cmd_names in sorted(self.command_names.iteritems()):
            cmd_names += version_cmd_names

        return cmd_names

    def add_commands(self, version, commands):
        # Add key if it doesn't exist
        if version not in self.command_names:
            self.command_names[version] = []
        # Add the commands that aren't duplicates
        self.command_names[version] += commands

root = append_angle_extensions(root)

all_commands = root.findall('commands/command')
all_cmd_names = GLCommandNames()

template_header_includes = """#include <GLES{major}/gl{major}{minor}.h>
#include <export.h>"""

template_sources_includes = """#include "libGLESv2/entry_points_gles_{}_autogen.h"

#include "libANGLE/Context.h"
#include "libANGLE/validationES{}{}.h"
#include "libGLESv2/global_state.h"
"""

gles1decls = {}

gles1decls['core'] = []
gles1decls['exts'] = {}

libgles_ep_defs = []
libgles_ep_exports = []

ordinal_start = 1

# First run through the main GLES entry points.  Since ES2+ is the primary use
# case, we go through those first and then add ES1-only APIs at the end.
for major_version, minor_version in [[2, 0], [3, 0], [3, 1], [1, 0]]:
    annotation = "{}_{}".format(major_version, minor_version)
    name_prefix = "GL_ES_VERSION_"

    is_gles1 = major_version == 1
    if is_gles1:
        name_prefix = "GL_VERSION_ES_CM_"

    comment = annotation.replace("_", ".")
    gles_xpath = ".//feature[@name='{}{}']//command".format(name_prefix, annotation)
    gles_commands = [cmd.attrib['name'] for cmd in root.findall(gles_xpath)]

    # Remove commands that have already been processed
    gles_commands = [cmd for cmd in gles_commands if cmd not in all_cmd_names.get_all_commands()]

    all_cmd_names.add_commands(annotation, gles_commands)

    decls, defs, libgles_defs, libgles_exports = get_entry_points(
        all_commands, gles_commands, ordinal_start, False)

    # Increment the ordinal before inserting the version comment
    ordinal_start += len(libgles_exports)

    # Write the version as a comment before the first EP.
    libgles_defs.insert(0, "\n// OpenGL ES {}.{}".format(major_version, minor_version))
    libgles_exports.insert(0, "\n    ; OpenGL ES {}.{}".format(major_version, minor_version))

    libgles_ep_defs += libgles_defs
    libgles_ep_exports += libgles_exports

    major_if_not_one = major_version if major_version != 1 else ""
    minor_if_not_zero = minor_version if minor_version != 0 else ""

    header_includes = template_header_includes.format(
        major=major_if_not_one, minor=minor_if_not_zero)

    # We include the platform.h header since it undefines the conflicting MemoryBarrier macro.
    if major_version == 3 and minor_version == 1:
        header_includes += "\n#include \"common/platform.h\"\n"

    source_includes = template_sources_includes.format(
        annotation.lower(), major_version, minor_if_not_zero)

    write_file(annotation, comment, template_entry_point_header,
               "\n".join(decls), "h", header_includes, "gl.xml")
    write_file(annotation, comment, template_entry_point_source,
               "\n".join(defs), "cpp", source_includes, "gl.xml")
    if is_gles1:
        gles1decls['core'] = get_gles1_decls(all_commands, gles_commands)


# After we finish with the main entry points, we process the extensions.
extension_defs = []
extension_decls = []

# Use a first step to run through the extensions so we can generate them
# in sorted order.
ext_data = {}

for gles1ext in gles1_extensions:
    gles1decls['exts'][gles1ext] = []

for extension in root.findall("extensions/extension"):
    extension_name = extension.attrib['name']
    if not extension_name in supported_extensions:
        continue

    ext_cmd_names = []

    # There's an extra step here to filter out 'api=gl' extensions. This
    # is necessary for handling KHR extensions, which have separate entry
    # point signatures (without the suffix) for desktop GL. Note that this
    # extra step is necessary because of Etree's limited Xpath support.
    for require in extension.findall('require'):
        if 'api' in require.attrib and require.attrib['api'] != 'gles2' and require.attrib['api'] != 'gles1':
            continue

        # Another special case for EXT_texture_storage
        filter_out_comment = "Supported only if GL_EXT_direct_state_access is supported"
        if 'comment' in require.attrib and require.attrib['comment'] == filter_out_comment:
            continue

        extension_commands = require.findall('command')
        ext_cmd_names += [command.attrib['name'] for command in extension_commands]

    ext_data[extension_name] = sorted(ext_cmd_names)

for extension_name, ext_cmd_names in sorted(ext_data.iteritems()):

    # Detect and filter duplicate extensions.
    dupes = []
    for ext_cmd in ext_cmd_names:
        if ext_cmd in all_cmd_names.get_all_commands():
            dupes.append(ext_cmd)

    for dupe in dupes:
        ext_cmd_names.remove(dupe)

    if extension_name in gles1_extensions:
        all_cmd_names.add_commands("glext", ext_cmd_names)
    else:
        all_cmd_names.add_commands("gl2ext", ext_cmd_names)

    decls, defs, libgles_defs, libgles_exports = get_entry_points(
        all_commands, ext_cmd_names, ordinal_start, False)

    # Avoid writing out entry points defined by a prior extension.
    for dupe in dupes:
        msg = "// {} is already defined.\n".format(dupe[2:])
        defs.append(msg)

    # Increment starting ordinal before adding extension comment
    ordinal_start += len(libgles_exports)

    # Write the extension name as a comment before the first EP.
    comment = "\n// {}".format(extension_name)
    defs.insert(0, comment)
    decls.insert(0, comment)
    libgles_defs.insert(0, comment)
    libgles_exports.insert(0, "\n    ; {}".format(extension_name))

    extension_defs += defs
    extension_decls += decls

    libgles_ep_defs += libgles_defs
    libgles_ep_exports += libgles_exports

    if extension_name in gles1_extensions:
        if extension_name not in gles1_no_context_decl_extensions:
            gles1decls['exts'][extension_name] = get_gles1_decls(all_commands, ext_cmd_names)

# Special handling for EGL_ANGLE_explicit_context extension
if support_EGL_ANGLE_explicit_context:
    comment = "\n// EGL_ANGLE_explicit_context"
    extension_defs.append(comment)
    extension_decls.append(comment)
    libgles_ep_defs.append(comment)
    libgles_ep_exports.append("\n    ; EGL_ANGLE_explicit_context")

    # Get the explicit context entry points
    decls, defs, libgles_defs, libgles_exports = get_entry_points(all_commands,
        all_cmd_names.get_all_commands(), ordinal_start, True)

    # Append the explicit context entry points
    extension_decls += decls
    extension_defs += defs
    libgles_ep_defs += libgles_defs
    libgles_ep_exports += libgles_exports

    # Generate .inc files for extension function pointers and declarations
    for major, minor in [[2, 0], [3, 0], [3, 1], [1, 0]]:
        annotation = "{}_{}".format(major, minor)

        major_if_not_one = major if major != 1 else ""
        minor_if_not_zero = minor if minor != 0 else ""
        version = "{}{}".format(major_if_not_one, minor_if_not_zero)

        glext_ptrs, glext_protos = get_glext_decls(all_commands,
            all_cmd_names.get_commands(annotation), version, True)

        glext_ext_ptrs = []
        glext_ext_protos = []

        # Append extensions for 1.0 and 2.0
        if(annotation == "1_0"):
            glext_ext_ptrs, glext_ext_protos = get_glext_decls(all_commands,
                all_cmd_names.get_commands("glext"), version, True)
        elif(annotation == "2_0"):
            glext_ext_ptrs, glext_ext_protos = get_glext_decls(all_commands,
                all_cmd_names.get_commands("gl2ext"), version, True)

        glext_ptrs += glext_ext_ptrs
        glext_protos += glext_ext_protos

        write_glext_explicit_context_inc(version, "\n".join(glext_ptrs), "\n".join(glext_protos))

header_includes = template_header_includes.format(
    major="", minor="")
header_includes += """
#include <GLES/gl.h>
#include <GLES/glext.h>
#include <GLES2/gl2.h>
#include <GLES2/gl2ext.h>
"""

source_includes = template_sources_includes.format("ext", "", "")
source_includes += """
#include "libANGLE/validationES.h"
#include "libANGLE/validationES1.h"
#include "libANGLE/validationES3.h"
#include "libANGLE/validationES31.h"
"""

write_file("ext", "extension", template_entry_point_header,
           "\n".join([item for item in extension_decls]), "h", header_includes,
           "gl.xml and gl_angle_ext.xml")
write_file("ext", "extension", template_entry_point_source,
           "\n".join([item for item in extension_defs]), "cpp", source_includes,
           "gl.xml and gl_angle_ext.xml")

write_context_api_decls("1_0", context_gles_header, gles1decls)

sorted_cmd_names = ["Invalid"] + [cmd[2:] for cmd in sorted(all_cmd_names.get_all_commands())]

entry_points_enum = template_entry_points_enum_header.format(
    script_name = os.path.basename(sys.argv[0]),
    data_source_name = "gl.xml and gl_angle_ext.xml",
    year = date.today().year,
    entry_points_list = ",\n".join(["    " + cmd for cmd in sorted_cmd_names]))

entry_points_enum_header_path = path_to("libANGLE", "entry_points_enum_autogen.h")
with open(entry_points_enum_header_path, "w") as out:
    out.write(entry_points_enum)
    out.close()

source_includes = """
#include "angle_gl.h"

#include "libGLESv2/entry_points_gles_1_0_autogen.h"
#include "libGLESv2/entry_points_gles_2_0_autogen.h"
#include "libGLESv2/entry_points_gles_3_0_autogen.h"
#include "libGLESv2/entry_points_gles_3_1_autogen.h"
#include "libGLESv2/entry_points_gles_ext_autogen.h"

#include "common/event_tracer.h"
"""

write_export_files("\n".join([item for item in libgles_ep_defs]), source_includes, "\n".join([item for item in libgles_ep_exports]))