bl_info = {
  'name': 'Blender - Discord Rich Presence',
  'description': 'Discord Rich Presence support for Blender',
  'author': 'Ace Asin',
  'version': (1, 0, 0),
  'blender': (2, 80, 0),
  'wiki_url': 'https://github.com/AceAsin/BlenderRPC',
  'tracker_url': 'https://github.com/AceAsin/BlenderRPC/issues',
  'warning': '',
  'support': 'COMMUNITY',
  'category': 'System',
}

import time, os, sys, pathlib
from .pypresence import pypresence as RPC

import bpy
import bpy.utils.previews
import webbrowser

from bpy.app.handlers import persistent

from . import Frontend
from . import Backend

Presence = RPC.Presence('566658117212045325')
Blender = 'blender'
Badge = 'badge'
Invite = 'discord.gg/U8vHS7y'
Time = None
Render = False
Frame = 0
Field = None
Preview = {}
Collection = None
Duration = time.time()
Path = os.path.join(os.path.dirname(os.path.normpath(bpy.app.tempdir)), 'BlendRpcPid')
Button = [{ 'label': 'Website', 'url': 'https://aceasin.com' }, { 'label': 'Discord', 'url': 'https://discord.gg/U8vHS7y' }]

class Discord(bpy.types.Operator):
  bl_idname = 'aceasin.discord'
  bl_label = 'Discord'
  bl_description = 'Become a part of my Discord community'
  bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

  def execute(self, context):
    webbrowser.open('https://discord.gg/U8vHS7y')

    self.report({'INFO'}, 'Discord opened')
    return {'FINISHED'}

class Gumroad(bpy.types.Operator):
  bl_idname = 'aceasin.gumroad'
  bl_label = 'Gumroad'
  bl_description = 'Support me by purchasing something on Gumroad'
  bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

  def execute(self, context):
    webbrowser.open('https://gumroad.com/AceAsin')

    self.report({'INFO'}, '')
    return {'FINISHED'}

class Patreon(bpy.types.Operator):
  bl_idname = 'aceasin.patreon'
  bl_label = 'Patreon'
  bl_description = 'Support me by becoming a Patron'
  bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

  def execute(self, context):
    webbrowser.open('https://patreon.com/AceAsin')

    self.report({'INFO'}, '')
    return {'FINISHED'}

class PayPal(bpy.types.Operator):
  bl_idname = 'aceasin.paypal'
  bl_label = 'PayPal'
  bl_description = 'Support me by donating to my PayPal'
  bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

  def execute(self, context):
    webbrowser.open('https://paypal.me/AceAsin')

    self.report({'INFO'}, '')
    return {'FINISHED'}

class KoFi(bpy.types.Operator):
  bl_idname = 'aceasin.kofi'
  bl_label = 'Ko-Fi'
  bl_description = 'Support me by buying me a coffee'
  bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

  def execute(self, context):
    webbrowser.open('https://ko-fi.com/AceAsin')

    self.report({'INFO'}, '')
    return {'FINISHED'}

class Documentation(bpy.types.Operator):
  bl_idname = 'aceasin.documentation'
  bl_label = 'Documentation'
  bl_description = 'Open the documentation'
  bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

  def execute(self, context):
    webbrowser.open('https://github.com/AceAsin/BlenderRPC')

    self.report({'INFO'}, '')
    return {'FINISHED'}

class Bug(bpy.types.Operator):
  bl_idname = 'aceasin.bug'
  bl_label = 'Bug'
  bl_description = 'Report a bug'
  bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

  def execute(self, context):
    webbrowser.open('https://github.com/AceAsin/BlenderRPC/issues')

    self.report({'INFO'}, '')
    return {'FINISHED'}

class Changelog(bpy.types.Operator):
  bl_idname = 'aceasin.changelog'
  bl_label = 'Changelog'
  bl_description = 'Open the changelog'
  bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

  def execute(self, context):
    webbrowser.open('https://github.com/AceAsin/BlenderRPC#readme')

    self.report({'INFO'}, '')
    return {'FINISHED'}

class Menu(bpy.types.Menu):
  bl_idname = 'aceasin.statemenu'
  bl_label = 'State Menu'

  def draw(self, context):
    layout = self.layout
    layout.label(text='State')

    layout.label(text='Test')
    layout.menu(StateSubMenu.bl_idname)

class SubMenu(bpy.types.Menu):
  bl_idname = 'aceasin.statesubmenu'
  bl_label = 'State Sub Menu'

  def draw(self, context):
    layout = self.layout
    layout.label(text='State')

    layout.label(text='Test')
    layout.label(text='Trash', icon='TRASH')
    layout.operator(KoFi.bl_idname)

classes = (
  Discord,
  Gumroad,
  Patreon,
  PayPal,
  KoFi,

  Documentation,
  Bug,
  Changelog,
)

def register():
  print('\n### Loading Blender RPC...')

  global Time

  bpy.utils.register_class(RpcPreferences)
  Time = time.time()
  Presence.connect()
  writePidFileAtomic()
  bpy.app.timers.register(updatePresenceTimer, first_interval=1.0, persistent=True)
  bpy.app.handlers.save_post.append(writePidHandler)
  # Rendering
  bpy.app.handlers.render_init.append(startRenderJobHandler)
  bpy.app.handlers.render_complete.append(endRenderJobHandler)
  bpy.app.handlers.render_cancel.append(endRenderJobHandler)
  bpy.app.handlers.render_post.append(postRenderHandler)
  # Operator
  for cls in classes:
    Frontend.make_annotations(cls)
    bpy.utils.register_class(cls)
  bpy.utils.register_class(Menu)
  bpy.utils.register_class(SubMenu)
  # Updater
  Frontend.register(bl_info)
  # Icon
  Collection = bpy.utils.previews.new()
  Root = os.path.dirname(__file__)
  Asset = os.path.join(Root, "Asset")
  Icon = os.path.join(Asset, "Icon")
  Image = { 'Discord' : 'Discord.png', 'Gumroad' : 'Gumroad.png', 'Patreon' : 'Patreon.png', 'PayPal' : 'PayPal.png', 'Ko-Fi' : 'Ko-Fi.png' }
  for Key, Extension in Image.items(): Collection.load(Key, os.path.join(Icon, Extension), 'IMAGE')
  Preview['Logo'] = Collection

def unregister():
  print('\n### Unlooading Blender RPC...')
  global Time

  Time = None
  Presence.close()
  removePidFile()
  bpy.app.timers.unregister(updatePresenceTimer)
  bpy.app.handlers.save_post.remove(writePidHandler)
  bpy.utils.unregister_class(RpcPreferences)
  # Rendering
  bpy.app.handlers.render_init.remove(startRenderJobHandler)
  bpy.app.handlers.render_complete.remove(endRenderJobHandler)
  bpy.app.handlers.render_cancel.remove(endRenderJobHandler)
  bpy.app.handlers.render_post.remove(postRenderHandler)
  # Operator
  for cls in reversed(classes):
    bpy.utils.unregister_class(cls)
  bpy.utils.unregister_class(Menu)
  bpy.utils.unregister_class(SubMenu)
  # Updater
  Frontend.unregister()
  # Icon
  print('UNLOADING ICONS!')
  for Collection in Preview.values(): bpy.utils.previews.remove(Collection)
  Preview.clear()
  print('DONE!')

def writePidFileAtomic():
  pid = os.getpid()
  Temporary = f'{Path}-{pid}'
  with open(Temporary, 'w') as tmpPidFile:
    tmpPidFile.write(str(pid))
    tmpPidFile.flush()
    os.fsync(tmpPidFile.fileno())
  os.replace(Temporary, Path)

def readPidFile():
  try:
    with open(Path, 'r') as pidFile:
      storedPid = int(pidFile.read())
  except OSError:
    return None
  except ValueError:
    return None
  return storedPid

def removePidFile():
  try:
    os.remove(Path)
  except OSError:
    pass

@persistent
def writePidHandler(*args):
  writePidFileAtomic()

@persistent
def startRenderJobHandler(*args):
  global Render
  global Time
  Render = True
  Time = time.time()

@persistent
def endRenderJobHandler(*args):
  global Render
  global Frame
  global Time
  Render = False
  Frame = 0
  Time = time.time()

@persistent
def postRenderHandler(*args):
  global Frame
  Frame += 1

def updatePresenceTimer():
  updatePresence()
  return 0

def updatePresence():
  # Pre-Checks
  readPid = readPidFile()
  if readPid is None:
    writePidFileAtomic()
  elif readPid != os.getpid():
    Presence.clear()
    return

  # Add-On Preferences
  Prefs = bpy.context.preferences.addons[__name__].preferences

  # List
  Counter = ['{Actions}', '{Armatures}', '{Brushes}', '{Cache Files}', '{Cameras}', '{Collections}', '{Curves}', '{Fonts}', '{Grease Pencils}', '{Images}', '{Lattices}', '{Libraries}', '{Lightprobes}', '{Lights}', '{Linestyles}', '{Masks}', '{Materials}', '{Meshes}', '{Metaballs}', '{Movieclips}', '{Node Groups}', '{Objects}', '{Paint Curves}', '{Palettes}', '{Particles}', '{Scenes}', '{Screens}', '{Shape Keys}', '{Sounds}', '{Speakers}', '{Texts}', '{Textures}', '{Window Managers}', '{Workspaces}', '{Worlds}']
  Extra = [['{Volumes}'], ['{Hairs}', '{Pointclouds}', '{Simulations}']]

  # Details
  if (Prefs.DetailsToggle and not Render or Prefs.DetailsToggle and not Prefs.RenderedDetails and Render):
    if (Prefs.CustomDetails == ''):
      Details = f'Project: {getProject()}' or 'Project: Untitled'
    else:
      Details = getCustom(Prefs.CustomDetails, Counter, Extra)
  elif (Prefs.DetailsToggle and Render):
    Details = f'Engine: {getRenderEngine()}'
  else: Details = None

  # State
  if (Prefs.StateToggle and not Render or Prefs.StateToggle and not Prefs.RenderedState and Render):
    if (Prefs.CustomState == ''):
      if (Prefs.StateToolbar == 'PRESET'):
        if Prefs.StatePreset == 'NONE': State = f'State: {None}'
        elif Prefs.StatePreset == 'OBJECT': State = f'Object: {getObject()}'
        elif Prefs.StatePreset == 'MODE': State = f'Mode: {getMode()}'
        elif Prefs.StatePreset == 'TYPE': State = f'Type: {getType()}'
        else: State = f'State: {None}'
      if (Prefs.StateToolbar == 'COUNTER'):
        for i in Counter:
          if (i == Prefs.StateCounter):
            State = f'{i}: {getCount(i)}'.replace('{', '').replace('}', '')
        for i in Extra[0]:
          if (i == Prefs.StateCounter):
            State = f'{i}: {getCount(i)}'.replace('{', '').replace('}', '')
        # for i in Extra[1]:
        #   if (i == Prefs.StateCounter):
        #     State = f'{i}: {getCount(i)}'.replace('{', '').replace('}', '')
    else:
      State = getCustom(Prefs.CustomState, Counter, Extra)
  elif (Prefs.StateToggle and Render):
    Range = getFrameRange()

    if (Frame > 0):
      State = f'Animation: Render Frame {Range[0]} / {Range[1]}'
    else:
      State = f'Image: Render Frame 1 / 1'
  else: State = None

  # Large
  if (Prefs.CustomLarge == ''):
    Large = f'{getBuild()} {getVersion()}'
  else:
    Large = getCustom(Prefs.CustomLarge, Counter, Extra)

  # Small
  if (Prefs.CustomSmall == ''):
    Small = 'Blender'
  else:
    Small = getCustom(Prefs.CustomSmall, Counter, Extra)

  # Timestamp
  if (Prefs.ElapsedTime and not Render or Prefs.ElapsedTime and not Prefs.RenderedTime and Render):
    Timestamp = Duration
  elif (Prefs.ElapsedTime and Render):
    Timestamp = Time
  else:
    Timestamp = None

  Presence.update(
    pid=os.getpid(),
    start=Timestamp,
    details=Details,
    state=State,
    large_image=Blender,
    large_text=Large,
    small_image=Badge,
    small_text=Small,
    buttons=Button
  )

def getCustom(Custom, Counter, Extra):
  Version = str(bpy.app.version[1])

  Layer = Custom

  if ('{Discord}' in Custom): Layer = Layer.replace('{Discord}', Invite + '\u200B')

  if ('{Project}' in Custom): Layer = Layer.replace('{Project}', getProject() + '\u200B')

  if ('{Build}' in Custom): Layer = Layer.replace('{Build}', getBuild() + '\u200B')
  if ('{Version}' in Custom): Layer = Layer.replace('{Version}', getVersion() + '\u200B')

  if ('{Object}' in Custom): Layer = Layer.replace('{Object}', getObject() + '\u200B')
  if ('{Mode}' in Custom): Layer = Layer.replace('{Mode}', getMode() + '\u200B')
  if ('{Type}' in Custom): Layer = Layer.replace('{Type}', getType() + '\u200B')

  for i in Counter:
    if i in Custom:
      Layer = Layer.replace(i, getCount(i) + '\u200B')

  for i in Extra[0]:
    if (i in Custom and Version != '80' or Version != '81' or Version != '81a' or Version != '82' or Version != '82a'):
      Layer = Layer.replace(i, getCount(i) + '\u200B')

  # for i in Extra[1]:
  #   if (i in Prefs.CustomState and Version != '80' or Version != '81' or Version != '81a' or Version != '82' or Version != '82a' or Version != '83'):
  #     Layer = Layer.replace(i, getCount(i) + '\u200B')

  return Layer + '\u200B'

def getProject():
  try:
    Name = bpy.path.display_name_from_filepath(bpy.data.filepath)
    if (Name == ''): return 'Untitled'
    else: return Name
  except:
    return 'Untitled'

def getObject():
  try:
    Object = bpy.context.view_layer.objects.active.name
    if (Object == ''): return 'Idle'
    else: return Object
  except:
    return 'Idle'

def getMode():
  try:
    Mode = bpy.context.view_layer.objects.active.mode
    if (Mode == ''): return 'Idle'
    elif (Mode == 'OBJECT'): return 'Object Mode'
    elif (Mode == 'EDIT'): return 'Edit Mode'
    elif (Mode == 'POSE'): return 'Pose Mode'
    elif (Mode == 'SCULPT'): return 'Sculpt Mode'
    elif (Mode == 'VERTEX_PAINT'): return 'Vertex Paint'
    elif (Mode == 'WEIGHT_PAINT'): return 'Weight Paint'
    elif (Mode == 'TEXTURE_PAINT'): return 'Texture Paint'
    elif (Mode == 'PARTICLE_EDIT'): return 'Particle Edit'
    elif (Mode == 'EDIT_GPENCIL'): return 'Edit Grease Pencil Strokes'
    elif (Mode == 'SCULPT_GPENCIL'): return 'Sculpt Grease Pencil Strokes'
    elif (Mode == 'PAINT_GPENCIL'): return 'Paint Grease Pencil Strokes'
    elif (Mode == 'WEIGHT_GPENCIL'): return 'Grease Pencil Weight Paint Strokes'
    else: return Mode
  except:
    return 'Idle'

def getType():
  try:
    Type = bpy.context.view_layer.objects.active.type
    if (Type == ''): return 'Idle'
    elif (Type == 'MESH'): return 'Mesh'
    elif (Type == 'CURVE'): return 'Curve'
    elif (Type == 'SURFACE'): return 'Surface'
    elif (Type == 'META'): return 'Meta'
    elif (Type == 'FONT'): return 'Font'
    elif (Type == 'ARMATURE'): return 'Armature'
    elif (Type == 'LATTICE'): return 'Lattice'
    elif (Type == 'EMPTY'): return 'Empty'
    elif (Type == 'GPENCIL'): return 'Grease Pencil'
    elif (Type == 'CAMERA'): return 'Camera'
    elif (Type == 'LIGHT'): return 'Light'
    elif (Type == 'SPEAKER'): return 'Speaker'
    elif (Type == 'LIGHT_PROBE'): return 'Light Probe'
    else: return Type
  except:
    return 'Idle'

def getCount(Data):
  if (Data == '{Actions}'): return str(len(bpy.data.actions))
  if (Data == '{Armatures}'): return str(len(bpy.data.armatures))
  if (Data == '{Brushes}'): return str(len(bpy.data.brushes))
  if (Data == '{Cache Files}'): return str(len(bpy.data.cache_files))
  if (Data == '{Cameras}'): return str(len(bpy.data.cameras))
  if (Data == '{Collections}'): return str(len(bpy.data.collections))
  if (Data == '{Curves}'): return str(len(bpy.data.curves))
  if (Data == '{Fonts}'): return str(len(bpy.data.fonts))
  if (Data == '{Grease Pencils}'): return str(len(bpy.data.grease_pencils))
  # if (Data == '{Hairs}'): return str(len(bpy.data.brushes)) #2.90
  if (Data == '{Images}'): return str(len(bpy.data.images))
  if (Data == '{Lattice}'): return str(len(bpy.data.lattices))
  if (Data == '{Libraries}'): return str(len(bpy.data.libraries))
  if (Data == '{Lightprobes}'): return str(len(bpy.data.lightprobes))
  if (Data == '{Lights}'): return str(len(bpy.data.lights))
  if (Data == '{Linestyles}'): return str(len(bpy.data.linestyles))
  if (Data == '{Masks}'): return str(len(bpy.data.masks))
  if (Data == '{Materials}'): return str(len(bpy.data.materials))
  if (Data == '{Meshes}'): return str(len(bpy.data.meshes))
  if (Data == '{Metaballs}'): return str(len(bpy.data.metaballs))
  if (Data == '{Movieclips}'): return str(len(bpy.data.movieclips))
  if (Data == '{Node Groups}'): return str(len(bpy.data.node_groups))
  if (Data == '{Objects}'): return str(len(bpy.data.objects))
  if (Data == '{Paint Curves}'): return str(len(bpy.data.paint_curves))
  if (Data == '{Palettes}'): return str(len(bpy.data.palettes))
  if (Data == '{Particles}'): return str(len(bpy.data.particles))
  # if (Data == '{Pointclouds}'): return str(len(bpy.data.brushes)) #2.90
  if (Data == '{Scenes}'): return str(len(bpy.data.scenes))
  if (Data == '{Screens}'): return str(len(bpy.data.screens))
  if (Data == '{Shape Keys}'): return str(len(bpy.data.shape_keys))
  # if (Data == '{Simulations}'): return str(len(bpy.data.brushes)) #2.90
  if (Data == '{Sounds}'): return str(len(bpy.data.sounds))
  if (Data == '{Speakers}'): return str(len(bpy.data.speakers))
  if (Data == '{Texts}'): return str(len(bpy.data.texts))
  if (Data == '{Textures}'): return str(len(bpy.data.textures))
  if (Data == '{Volumes}'): return str(len(bpy.data.volumes)) # 2.83
  if (Data == '{Window Managers}'): return str(len(bpy.data.window_managers))
  if (Data == '{Workspaces}'): return str(len(bpy.data.workspaces))
  if (Data == '{Worlds}'): return str(len(bpy.data.worlds))

def getBuild():
  Build = {
    'alpha': 'Alpha',
    'beta': 'Beta',
    'rc': 'Release Candidate',
    'release': 'Release'
  }.get(bpy.app.version_cycle, '')
  return Build

def getVersion():
  Version = bpy.app.version_string
  return Version

def getPreset():
  Preset = [
    ('OBJECT', 'Object', 'It will display the active object name'),
    ('MODE', 'Mode', 'It will display the active object mode'),
    ('TYPE', 'Type', 'It will display the active object type')
  ]
  return Preset

def getProps():
  Description = ['Show', 'on state']

  Count = [
    ('{Actions}', 'Actions', f'{Description[0]} action count {Description[1]}'),
    ('{Armatures}', 'Armatures', f'{Description[0]} armature count {Description[1]}'),
    ('{Brushes}', 'Brushes', f'{Description[0]} brush count {Description[1]}'),
    ('{Cache Files}', 'Cache Files', f'{Description[0]} cache file count {Description[1]}'),
    ('{Cameras}', 'Cameras', f'{Description[0]} camera count {Description[1]}'),
    ('{Collections}', 'Collections', f'{Description[0]} collection count {Description[1]}'),
    ('{Curves}', 'Curves', f'{Description[0]} curve count {Description[1]}'),
    ('{Fonts}', 'Fonts', f'{Description[0]} font count {Description[1]}'),
    ('{Grease Pencils}', 'Grease Pencils', f'{Description[0]} grease pencil count {Description[1]}'),
    ('{Images}', 'Images', f'{Description[0]} image count {Description[1]}'),
    ('{Lattices}', 'Lattices', f'{Description[0]} lattice count {Description[1]}'),
    ('{Libraries}', 'Libraries', f'{Description[0]} library count{Description[1]}'),
    ('{Lightprobes}', 'Lightprobes', f'{Description[0]} lightprobe count {Description[1]}'),
    ('{Lights}', 'Lights', f'{Description[0]} light count {Description[1]}'),
    ('{Linestyles}', 'Linestyles', f'{Description[0]} linestyle count {Description[1]}'),
    ('{Masks}', 'Masks', f'{Description[0]} mask count {Description[1]}'),
    ('{Materials}', 'Materials', f'{Description[0]} material count {Description[1]}'),
    ('{Meshes}', 'Meshes', f'{Description[0]} mesh count {Description[1]}'),
    ('{Metaballs}', 'Metaballs', f'{Description[0]} metaball count {Description[1]}'),
    ('{Movieclips}', 'Movieclips', f'{Description[0]} movieclip count {Description[1]}'),
    ('{Node Groups}', 'Node Groups', f'{Description[0]} node group count {Description[1]}'),
    ('{Objects}', 'Objects', f'{Description[0]} object count {Description[1]}'),
    ('{Paint Curves}', 'Paint Curves', f'{Description[0]} paint curve count {Description[1]}'),
    ('{Palettes}', 'Palettes', f'{Description[0]} pallete count {Description[1]}'),
    ('{Particles}', 'Particles', f'{Description[0]} particle count {Description[1]}'),
    ('{Scenes}', 'Scenes', f'{Description[0]} scene count {Description[1]}'),
    ('{Screens}', 'Screens', f'{Description[0]} screen count {Description[1]}'),
    ('{Shape Keys}', 'Shape Keys', f'{Description[0]} shape key count {Description[1]}'),
    ('{Sounds}', 'Sounds', f'{Description[0]} sound count {Description[1]}'),
    ('{Speakers}', 'Speakers', f'{Description[0]} speaker count {Description[1]}'),
    ('{Texts}', 'Texts', f'{Description[0]} text count {Description[1]}'),
    ('{Textures}', 'Textures', f'{Description[0]} texture count {Description[1]}'),
    ('{Window Managers}', 'Window Managers', f'{Description[0]} window manager count {Description[1]}'),
    ('{Workspaces}', 'Workspaces', f'{Description[0]} workspace count {Description[1]}'),
    ('{Worlds}', 'Worlds', f'{Description[0]} world count {Description[1]}'),
  ]

  Extra = [
    [
      ('{Volumes}', 'Volumes', f'{Description[0]} volume count {Description[1]}'), # 2.83
    ],
    [
      # ('HAIRS', 'Hairs', f'{Description[0]} hair count {Description[1]}'), # 2.90
      # ('POINTCLOUDS', 'Pointclouds', f'{Description[0]} pointcloud count {Description[1]}'), # 2.90
      # ('SIMULATIONS', 'Simulations', f'{Description[0]} simulation count {Description[1]}'), # 2.90
    ]
  ]

  Version = str(bpy.app.version[1])

  if (Version == '80' or Version == '81' or Version == '81a' or Version == '82' or Version == '82a'):
    return Count
  elif (Version == '83'):
    return sorted(Count + Extra[0])
  else:
    return sorted(Count + Extra[0] + Extra[1])

def getRenderEngine():
  internalName = bpy.context.engine
  internalNameStripped = internalName.replace('BLENDER_', '').replace('_', ' ')
  return internalNameStripped.title()

def getFrameRange():
  start = bpy.context.scene.frame_start
  end = bpy.context.scene.frame_end
  cursor = bpy.context.scene.frame_current
  return (cursor - start + 1, end - start + 1)

def updateCustom(self, context):
  updatePresence()

def TargetVersion(self, context):

	if Backend.updater.invalidupdater == True:
		ret = []

	ret = []
	i=0
	for tag in Backend.updater.tags:
		ret.append( (tag,tag,'Select to install '+tag) )
		i+=1
	return ret

class RpcPreferences(bpy.types.AddonPreferences):
  bl_idname = __name__

  Target: bpy.props.EnumProperty(
    name='Target',
    description='Select the version to install',
    items=TargetVersion
  )

  DetailsToggle: bpy.props.BoolProperty(
    name = 'Details Toggle',
    default = True
  )

  StateToggle: bpy.props.BoolProperty(
    name = 'State Toggle',
    default = True
  )

  ElapsedTime: bpy.props.BoolProperty(
    name='Elapsed Time',
    default=True,
  )

  RenderedDetails: bpy.props.BoolProperty(
    name='Rendered Details',
    default=True
  )

  RenderedState: bpy.props.BoolProperty(
    name='Rendered State',
    default=True
  )

  RenderedTime: bpy.props.BoolProperty(
    name='Rendered Time',
    default=True,
  )

  StateToolbar: bpy.props.EnumProperty(
    name='State Toolbar',
    items=[
          ('PRESET', 'Preset', 'Show preset state options'),
          ('COUNTER', 'Counter', 'Show counter state options')
    ],
    description='',
    default='PRESET'
  )

  CustomDetails: bpy.props.StringProperty(
    name = 'Custom Details',
    description = 'Custom details with optional variables',
    default = '',
    update = updateCustom
  )

  CustomState: bpy.props.StringProperty(
    name = 'Custom State',
    description = 'Custom state with optional variables',
    default = '',
    update = updateCustom
  )

  CustomLarge: bpy.props.StringProperty(
    name = 'Large Text',
    description = 'Custom large image hover text with optional variables',
    default = '',
    update = updateCustom
  )

  CustomSmall: bpy.props.StringProperty(
    name = 'Small Text',
    description = 'Custom small image hover text with optional variables',
    default = '',
    update = updateCustom
  )

  StatePreset: bpy.props.EnumProperty(
    name='State Preset',
    items = getPreset()
  )

  StateCounter: bpy.props.EnumProperty(
    name='State Counter',
    items = getProps()
  )

  def draw(self, context):
    layout = self.layout

    Frontend.update_settings_ui(self, context) # FILE_FOLDER

    #########
    # START #
    #########

    row = layout.row(align=True)
    col1 = row.column(align=True)
    col1.label(text='Toggle:')
    col2 = row.column(align=True)
    col2.alignment = 'RIGHT'
    col2.label(icon='PREFERENCES') # TOOL_SETTINGS

    row = layout.row()

    col = row.column(align = True)

    toggle = col.row(align=True)
    toggle.label(text='Elapsed: Details')
    toggle.prop(self, 'DetailsToggle', text = '', toggle=True)

    toggle = col.row(align=True)
    toggle.label(text='Elapsed: State')
    toggle.prop(self, 'StateToggle', text = '', toggle=True)

    toggle = col.row(align=True)
    toggle.label(text='Elapsed: Time')
    toggle.prop(self, 'ElapsedTime', text='', toggle=True)

    col = row.column(align = True)

    toggle = col.row(align=True)
    toggle.label(text='Rendered: Details')
    toggle.prop(self, 'RenderedDetails', text='', toggle=True)

    toggle = col.row(align=True)
    toggle.label(text='Rendered: State')
    toggle.prop(self, 'RenderedState', text='', toggle=True)

    toggle = col.row(align=True)
    toggle.label(text='Rendered: Time')
    toggle.prop(self, 'RenderedTime', text='', toggle=True)

    #######
    # End #
    #######

    #########
    # START #
    #########

    row = layout.row(align=True)
    col1 = row.column(align=True)
    col1.label(text='Options:')
    col2 = row.column(align=True)
    col2.alignment = 'RIGHT'
    col2.label(icon='PINNED')

    toolbar = layout.row(align = True)
    toolbar.prop(self, 'StateToolbar', text='State Toolbar', expand=True)

    row = layout.row(align = True)
    if (bpy.context.preferences.addons[__name__].preferences.StateToolbar == 'PRESET'):
      row.label(text = 'Preset: State')
      row.prop(self, 'StatePreset', text = '')
    if (bpy.context.preferences.addons[__name__].preferences.StateToolbar == 'COUNTER'):
      row.label(text = 'Counter: State')
      row.prop(self, 'StateCounter', text = '')

    #######
    # END #
    #######

    #########
    # START #
    #########

    row = layout.row(align=True)
    col1 = row.column(align=True)
    col1.label(text='String:')
    col2 = row.column(align=True)
    col2.alignment = 'RIGHT'
    col2.label(icon='OPTIONS')

    row = layout.row(align = True)
    row.label(text = 'Custom: Details')
    row.prop(self, 'CustomDetails', text = '')

    row = layout.row(align = True)
    row.label(text = 'Custom: State')
    row.prop(self, 'CustomState', text = '') # RESTRICT_VIEW_ON / RESTRICT_VIEW_OFF / TRACKER / PINNED / OPTIONS

    row = layout.row(align = True)
    row.label(text = 'Custom: Large')
    row.prop(self, 'CustomLarge', text = '')

    row = layout.row(align = True)
    row.label(text = 'Custom: Small')
    row.prop(self, 'CustomSmall', text = '')

    #######
    # END #
    #######

    row = layout.row(align=True)
    col1 = row.column(align=True)
    col1.label(text='Developer: Ace Asin')
    col2 = row.column(align=True)
    col2.alignment = 'RIGHT'
    col2.label(icon='URL')

    # row = layout.row()
    # row.alert = True
    # row = row.grid_flow(even_columns=True)
    # row.operator(Documentation.bl_idname, text='', icon='HELP', depress=False)
    # row.operator(Bug.bl_idname, text='', icon='GHOST_ENABLED', depress=False)
    # row.operator(Changelog.bl_idname, text='', icon='TEXT', depress=False)

    # row = layout.row(align=True)
    # col1 = row.column(align=True)
    # col1.label(text='Support: Ace Asin')
    # col2 = row.column(align=True)
    # col2.alignment = 'RIGHT'
    # col2.label(icon='FUND')

    row = layout.row()
    row = row.grid_flow(even_columns=True)
    row.operator(Discord.bl_idname, text='', icon_value=Preview['Logo']['Discord'].icon_id)
    row.operator(Gumroad.bl_idname, text='', icon_value=Preview['Logo']['Gumroad'].icon_id)
    row.operator(Patreon.bl_idname, text='', icon_value=Preview['Logo']['Patreon'].icon_id)
    row.operator(PayPal.bl_idname, text='', icon_value=Preview['Logo']['PayPal'].icon_id)
    row.operator(KoFi.bl_idname, text='', icon_value=Preview['Logo']['Ko-Fi'].icon_id)