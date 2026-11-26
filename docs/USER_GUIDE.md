# LevelGen user guide

## LevelGen panel presets

Open **LevelGen** from the editor's **Window** menu or toolbar. Pick **Hub and Wings**, **Compact Vertical**, **Long Corridor**, **Arena**, or **Maze**, then click **Generate level**. The cards show minimaps for seed 42, with Compact Vertical showing the ground floor. Scroll the cards horizontally in a narrow dock.

Selecting a card fills the generator's settings, including its seed, meshes, and theme, for the next generation. In an empty map, the panel holds those settings until you click Generate level. You can edit the seed in the panel or adjust a placed generator in Details.

Click **Save current as preset** to save the settings as a **Level Gen Preset** data asset. You can edit that asset or create one directly through **Content Browser > Add > Miscellaneous > Data Asset**. Supply a display name and an optional texture for its card. Keep presets in project content or in an enabled theme pack's content. Click **Refresh presets** to discover new assets or update the cards after editing them.

## Advanced settings in the LevelGen panel

Open **Details** when you want to adjust **Layout**, **Rooms**, **Streaming**, **Multiplayer**, or **Performance tier**. Expand a group to see its settings. **Reset group** restores that group's defaults. With **Live preview** on, the panel refreshes the minimap as you edit. Click **Generate level** to apply the changes to the level.

## Open the demo in Unreal Engine 5.8

1. Open `ue5/LevelGenHost/LevelGenHost.uproject`. The host enables LevelGen and the Python Editor Script Plugin.
2. If the Content Browser already has **LevelGenDemo → LevelGenDemo**, open that map. Otherwise, save your current level, open **Window → Developer Tools → Output Log**, and enter this command to create the map and theme.

   ```text
   py "C:/AZI/LevelGen/ue5/LevelGenHost/Content/Python/create_levelgen_demo.py"
   ```

   Change the path if your checkout is elsewhere. The script saves the map and **BasicShapesTheme** under `/Game/LevelGenDemo`.
3. Select **LevelGen Demo Generator** in the Outliner. The demo uses seed 42, the Small preset, one-metre cells, and Ultra quality. It uses the engine's plane for floors, cube for walls and crates, and cylinder for drums.
4. Click **Generate** to refresh the saved demo preview with the current wall height. Change **Quality** and click **Generate** to compare tiers.
5. Use **Play** with **Spawn Player At → Default Player Start**. The demo uses Unreal's default flying pawn. Use WASD and the mouse to explore from the seed 42 start room. Regenerate with seed 42 before testing the authored spawn if you changed the layout.

## Try Hub and Wings and the elevator

Open **LevelGenDemo_HubAndWings** under **LevelGenDemo**. If the map is missing, run the demo script above with `--hub` after the closing quote. It saves the new map and its empty **LevelGenRoomTemplate** alongside the basic demo.

Play from **Default Player Start** to explore the seed-7 entrance and three wings. Enter `stat levels` in the play console to see room instances load and unload as you move. The circular final room lies beyond the middle wing.

The three-stop elevator is in the separate sample west of the hub. To start nearby, stop play, select **Three-Stop Elevator Sample** in the Outliner and press **F** to locate it, then right-click the bottom-floor entry room on the west end of the sample and choose **Play From Here**. Fly to the middle room, aim at a button cube and press **E** within 250 cm. The landing button calls the car. Use the two buttons on the car to go down or up. The demo uses the default flying pawn, so use the mouse and WASD to follow the platform between floors.

## Try Compact Vertical

Open **LevelGenDemo_Vertical** under **LevelGenDemo**. If the map is missing, run the demo script above with `--vertical` after the closing quote. It saves the map and the empty streaming template. Play from **Default Player Start**. Follow the perimeter or take the catwalk across the two atriums. The stairs are in the northwest room, the ladder is in the southeast room, and the elevator is in the north landing. Stand beside the ladder and press **E** to move up one landing or **Q** to move down. The ladder uses an immediate transfer between landings. For the elevator, aim at a button and press **E**.

Choose **Compact Vertical** and set **Compact Floors** to 3, 4, or 5. The preset groups the complete geometry, dressing, and story for each floor into its own chunk. Enable **Stream Rooms** and assign an empty **Room Level Template** to load and unload each floor independently in play. The engine checks vertical distance as well as the horizontal radius and preloads neighboring decks for connector travel. The demo enables this option. The elevator serves all chunks from the persistent generator.

Ultra and High add shelves, upper-wall panels, hanging props, pipes, beams, ledge lights, and stacked crates using the engine's basic shapes. Potato keeps the structure and core theme props. Blueprints can read **Floor Roles** or call **Use Vertical Ladder** beside a landing. The **Narrative** toggle still uses a room table authored for the chosen floor count if you want the full room director.

## Set up your own level

Enable LevelGen in your UE 5.8 project. In a level, place a **Level Gen Actor**, assign **Floor Mesh** and **Wall Mesh**, then click **Generate** in Details. Use **Clear** to remove the generated content. Save the level to keep the preview.

Use meshes sized to the grid in plan view, with floor and wall pivots centred on the cell. Put the floor's walkable surface at its pivot height. Floors keep their authored thickness. LevelGen fits each wall mesh's vertical bounds from the floor plane to **Wall Height**. The actor's origin marks the grid corner, and the grid follows the actor's local X and Y axes. For a doorway frame, put its pivot at the centre of the opening and point its local X axis across the opening.

In Blueprint, call **Generate** to create a level and listen for **On Generated** to get the start and exit world positions. If Generate fails, open the Output Log to see the reason.

## Options in Details

| Option | What it changes |
| --- | --- |
| Seed | Reuse the same seed and inputs to repeat a level. Change the seed for another layout. |
| Preset | Small, Medium, and Dense generate BSP dungeons. Custom uses the Settings below. Hub and Wings, Elevator Shaft, and Compact Vertical use graph templates. |
| Elevator Stops, Elevator Floor Height, Elevator Class | Set the number of landings, their vertical spacing in centimetres, and an optional Blueprint elevator subclass. Elevator Stops applies to Elevator Shaft. Compact Vertical uses **Compact Floors** and supports spacing from 300 to 600 cm. |
| Cell Size | Length of one grid cell in millimetres. Enter 2000 for two metres. |
| Settings | Width and Height set the grid size. Room Count is the exact target. Min Room Size and Max Room Size set the bounds for both room dimensions. Corridor Width cannot exceed Min Room Size. Loop Rate ranges from 0 to 10,000, where 10,000 always adds an extra connection when the generator has the opportunity. |
| Floor Mesh, Wall Mesh, Doorway Mesh | Set the architecture. Leave Doorway Mesh blank for open passages without frames. |
| Wall Height | Height above each floor in centimetres, 300 by default. Applies to every quality tier on the next Generate. |
| Theme | Choose prop meshes and placement rules. Edit each prop's **Density** in the theme to control how often it is tried. |
| Enable Interactables | Spawn props with an Interactable Class as actors. Turn it off to show those same props as mesh instances. |
| Enable Story, Story Table | Place beats from the assigned table the next time you generate. |
| Stream Rooms | Generate standalone play content in one dynamic level instance per loaded room. Off by default. |
| Room Level Template | Empty non-partitioned map to instance for each room. See setup below. |
| Room Load Radius | Horizontal preload distance in centimetres. Potato uses half this value, capped by Potato Room Distance. |
| Quality | Choose how much dressing to show. See the tiers below. |
| Potato Room Distance | Caps the Potato streaming radius. It also controls when loaded story and interactable visuals hide, and when room-owned instances hide with streaming off. Both distances are in centimetres. |
| Potato Min LOD | Minimum LOD index for generated static meshes in Potato. Use 0 to keep their existing LOD settings. |
| Potato Texture Max Size | Maximum texture width or height in pixels for generated static mesh materials during Potato gameplay. Defaults to 512. Set 0 to disable. |
| Potato Material Overrides | Optional map from an oversized material to a cap-compliant Potato material. Enable the appropriate mesh usage on replacements, including Instanced Static Meshes for generated batches. |
| Potato Floor Mesh, Potato Wall Mesh, Potato Doorway Mesh | Optional cheaper versions of the architecture. An empty slot uses the regular mesh. |

For Custom settings, the grid must have room for the requested rooms and their one-cell margins. If generation fails, try a larger grid, fewer rooms, or a smaller minimum room size.

## Auto Lights

Enable **Auto Lights** and click **Generate** to add one light near the top of each room. A theme can override the point or spot light, color, and output in lumens under **Room Lights**. Use the narrative room type as the key when Narrative is enabled. Rooms without a narrative type use **Entrance**, **Exit**, or **Standard**. Unmatched types use **Default Room Light**. With no theme, rooms use warm point lights and the exit uses a warm spotlight.

**Corridor Light Spacing** defaults to six cells. Lights follow corridor cells, with spacing measured in steps along the corridor floor, including turns and junctions. **Corridor Light** in the theme sets their style. Ultra, High, and Medium use room and corridor lights. Potato keeps only room lights and disables their shadows. **Set Quality** updates the lights on the current layout, and **Clear** removes them.

## Bake a generated level

Generate the level in the editor at the quality tier you want to keep. Select one generator and open **LevelGen → Bake** in Details. Set **Bake Mode**, then click **Bake**.

- **Static Mesh Actors** creates one editable actor for each current mesh instance.
- **Packed Level Actors** stores geometry in instanced components on one Packed Level Actor per room with geometry. Shared geometry goes to the nearest room. Edit the packed components on the actor in the map.

Story beats become standalone actors with their **Level Gen Story Beat** component and text. Interactables keep their actor classes and editable properties. Vertical layouts keep their elevator as a standalone actor. Generator-driven room streaming, narrative progression, quality switching, and **Use Vertical Ladder** end when you bake. Generate again before using Packed Level Actors on a Compact Vertical preview saved by an older plugin version.

Editor Utility Blueprints can set **Bake Mode** and call **Bake** on a **Level Gen Actor**. The call returns true when the output is baked into the generator's level. Bake is available in the editor before play and clears and disables generation on that actor. Use **Undo** to remove the baked actors and restore the generated preview. Save the level to keep the baked result.

## Quality tiers and Potato mode

| Tier | Dressing shown |
| --- | --- |
| Ultra | All core, detail, and clutter props. Nanite is available on meshes configured for it. |
| High | Core, detail, and every second clutter placement. |
| Medium | Core and detail. |
| Potato | Core. Generated mesh instances have Nanite disabled and use the Potato LOD and mesh options. |

Call **Set Quality** from Blueprint to switch tiers in play. The layout and prop positions are preserved. Returning to Ultra restores the same dressing placements. **Set Interactables Enabled** switches between interactable actors and mesh instances. An actor that is removed and later restored starts fresh.

Potato builds only walls next to room or corridor floor, including diagonally. With **Stream Rooms** off, room floors, room-owned walls, regular dressing, story meshes, and the static mesh visuals of eligible interactables hide beyond **Potato Room Distance** from all local player views. The distance check leaves collision and actor state active. Optional Potato meshes should match the original pivot and collision.

In PIE or a packaged game, LevelGen checks the reported width and height of textures used by generated static mesh materials when it applies Potato quality. If a material exceeds the cap, it uses a compliant material from **Potato Material Overrides** or the engine default surface material if it fits. If no compliant surface is available or an overlay exceeds the cap, the mesh hides with its collision intact. Returning to a higher tier restores the original materials and rendering settings. Call **Set Quality** again after changing the cap, changing material overrides, or assigning new gameplay materials. Shared textures keep their authored resolution and can remain resident through other references.

## Stream rooms during play

1. Create a separate **Empty Level** map with World Partition disabled, no placed actors, and an empty Level Blueprint. Save it in your project content. You can share this template across generators.
2. In your gameplay map, assign that map to **Room Level Template**, enable **Stream Rooms**, and click **Generate**. The editor shows the full preview. Generate again after changing the toggle or template.
3. Play in standalone or single-player PIE. Set **Room Load Radius** high enough for your movement speed so the next chunk finishes loading before you reach it. For a packaged game, include the template in **Project Settings > Packaging > List of maps to include in a packaged build**.

LevelGen uses UE 5.8 dynamic level instances because the seed can define new rooms during play. Each active instance contains its room's floor, walls, dressing, story beats, interactables, and a share of the corridors. LevelGen assigns corridor and solid cells to the closest room floor by grid distance, so intersections have one owner. Its load region covers the room, assigned walkable tiles, and their bordering walls. A doorway frame belongs to the room on its room-floor side.

LevelGen checks horizontal distance to those bounds from each local pawn and camera. It loads the start area asynchronously when play begins and keeps the full preview geometry and collision until the initial chunks are visible. If startup streaming fails or takes more than 15 seconds, play continues with the full layout. Loaded chunks have an extra two metres beyond the load radius to reduce repeated loads near a boundary. Potato uses the smaller of half the normal radius and **Potato Room Distance**. Chunk unloading removes geometry, collision, and actors. Reloading recreates interactables in their initial state. The generator retains placement data and references to shared mesh assets. Networked sessions use the full generated layout.

An authored Level Streaming Volume controls existing sublevels from a persistent map. World Partition's runtime grid is prepared from authored world content. Dynamic instances give each runtime-generated room its own actual streamed sublevel while letting LevelGen calculate the equivalent load region from the seed and change its radius by quality tier. [Dynamic level instance API](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/ULevelStreamingDynamic/LoadLevelInstanceBySoftObjectPtr), [Level Streaming Volumes](https://dev.epicgames.com/documentation/en-us/unreal-engine/level-streaming-using-volumes-in-unreal-engine), [World Partition](https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine)

## Make a theme

1. In the Content Browser, choose **Add → Miscellaneous → Data Asset → Level Gen Theme**.
2. Add entries under **Props** and give each one a unique lowercase **Id**, such as `wooden-crate`. Assign a **Mesh** with its pivot centred on the footprint at floor height.
3. Set **Width** and **Height** to the number of cells the mesh covers before rotation. Set **Allowed Tags** to one or more places to try it, such as **Corner**, **Wall Edge**, or **Center**. The whole prop must fit inside a room. LevelGen reserves routes between doorways and the start and exit.
4. Pick a **Tier**. Use Core for the large props that make a room recognizable, Detail for secondary pieces, and Clutter for small extras. Set **Density** from 0 to 10,000. For example, 2,500 gives a matching cell a 25% chance of trying the prop. Clearance, available floor space, and **Max Per Room** can reduce the final count.
5. Add the allowed **Rotations** from 0, 90, 180, and 270 degrees. Use **Clearance** to keep extra cells around the mesh free of other props. Add a **Potato Mesh** if you have a cheaper version.
6. For an interactive prop, make a Blueprint based on **Level Gen Pickup**, **Door**, **Container**, **Light Switch**, or **Breakable**. Put its behavior in **Event On Interact**, select the Blueprint in **Interactable Class**, and call **Interact** from your game's interaction logic.
7. Assign the new **Theme** to the actor and click **Generate**. Try a few seeds and each quality tier to check fit, coverage, and walkable space.

To add story, create a **Level Gen Story Table** data asset. Give each entry a unique **Prop Id**, a **Text Id**, display **Text**, and a one-cell mesh. Choose **Note** for the start room, **Set Piece** for the exit, or **Key Item** for a side room. Assign the table, turn **Enable Story** on, and click **Generate**. The generator uses available space after dressing, and Blueprints can read the text from the generated Level Gen Story Beat components.

## Elevator shaft

Select **Elevator Shaft** in the Level Gen Actor preset menu. Set **Elevator Stops** (three by default) and **Elevator Floor Height** (400 cm by default). Match the height to your wall meshes and leave enough clearance for your character. Use floor meshes whose collision fits one cell, with the walkable surface at the pivot height. Generate to preview the stacked rooms, shaft openings, and platform. Generated start and exit sit on the bottom and top floor, respectively. Landing rooms stay clear of props and story markers.

During play, aim at a landing button next to the opening and call **Interact** using your game's interaction trace. Once the platform arrives, step on and use the two cab buttons. Facing local +Y, the left button goes down and the right button goes up. At each end of the shaft only one direction is available. Travel requests are accepted while the platform is idle. A level designer can add gates or railings around open landings to suit the game's movement and interaction rules.

For custom behavior, assign an **Elevator Class** derived from **Level Gen Elevator**. Implement **Event On Quick Time Event** to react to departure. It receives the zero-based origin and destination stops. Use **Request Stop** to wire additional controls and **Is Traveling** to drive UI.

## Narrative director

Use **Narrative** with a **Level Gen Narrative Table** data asset. Paste a narrative JSON document into the asset's **Table Json** field and assign it to the actor's **Narrative Table** setting. For the Hub and Wings preset, start with [Mind Space](../themes/mindspace-narrative.json). For the Elevator Shaft preset with three stops, try [The Hill Relay](../themes/relay-narrative.json). Enable **Narrative** and click **Generate**. Tables must match the selected layout's node keys.

The actor exposes **Run Synopsis**, **Narrative Event**, **Narrative Ending**, and **Narrative Rooms**. Each room component carries its global room ID, stable node key, role, area, type, objective, encounter, lore and progression fields. Components stay on the generator while rooms stream. **Clear** and regeneration reset the synopsis, components and gate progress.

Call **Complete Narrative Gate** with the gate's node ID from the Blueprint that resolves its objective. Use **Is Narrative Final Unlocked** when initializing a final-room door or encounter, and bind **On Narrative Final Unlocked** to activate it when the last required gate is completed. The game Blueprint supplies the doors, encounters and interactions.

## Navigation and spawn points

**Build NavMesh** defaults to on. Click **Generate** to create a Nav Mesh Bounds Volume around the generated level. While playing with **Stream Rooms** on, navigation tiles update as room geometry loads and unloads. For runtime generation and room streaming, set **Project Settings > Navigation Mesh > Runtime Generation** to **Dynamic**. The host project already uses this setting. Use floor and wall meshes with collision and size the corridors for your navigation agent.

Bind **On Level Generated** on the generator to receive world-space start and exit positions and read the **Spawn Points** array. The event fires once per successful Generate call after the markers exist and navigation has been requested. Runtime navigation tiles may still be building when the event fires.

Each **Level Gen Spawn Point** exposes its **Type**, **Room Id**, **Node Id**, and **Content Id**. The player start marker comes from the layout. With **Narrative** on, resolved encounters supply enemy markers and narrative pickups supply loot markers. Use Content Id to choose the enemy or pickup to spawn in your Blueprint. Markers remain available while rooms stream. **Clear** removes the generated markers and bounds volume.

## Minimap export

Generate a layout, then open **LevelGen | Minimap** in the actor's Details panel. Set **Minimap Pixels Per Cell** from 1 to 16 (default 4) and click **Export Minimap PNG**. The default output is `Saved/Minimaps/Minimap.png` in your project. **Minimap PNG Path** accepts a path relative to `Saved` or an absolute path. Exports replace files at the chosen names.

In Blueprint, call **Export Minimap** after generation. The node returns a success flag and an array of transient `Texture2D` objects ordered from the lowest floor up. Leave **Png Path** empty for texture output alone, or supply it to write PNGs as well. Keep the returned textures in a Blueprint variable or assign them to a widget. The export uses the current generated snapshot, including any placed story beats. Regenerate older saved layouts once to create the minimap snapshot.

Room floor is light gray, corridor floor is blue-gray, walls are dark, and door thresholds are amber. Green marks start, red marks exit, cyan marks a shared start and exit, and purple marks story beats. Compact Vertical openings are transparent. A stack writes `Minimap-floor-1.png`, `Minimap-floor-2.png`, and so on.

### Preview seeds in Details

Select one Level Gen Actor and click **Preview next 6 seeds** in **LevelGen**. The picker shows the six seeds after the actor's current seed and wraps to zero after 4,294,967,295. Each card shows its floors from lowest to highest. Click a card to set the seed and regenerate in one undoable action. Close the picker to keep the current level.

## Generate in multiplayer

Enable **Replicates** in the Level Gen Actor's **Replication** settings. On the server, choose **Seed** and the generation options, then call **Generate**. Clients, including late joiners, receive those inputs and build the layout locally. Call **Clear** on the server to clear the layout on clients. Call **Generate** again to publish a new seed or new generation options.

Assign shared, cooked assets for meshes, themes, story and narrative tables, and classes. Multiplayer uses the full generated layout with room streaming inactive. Custom gameplay state such as opened doors, elevator position, and completed narrative gates needs its own multiplayer implementation. Keep locally generated child actor classes nonreplicating to avoid spawning duplicate actors on clients.

## PCG graphs

Enable **LevelGen PCG** in the Plugins window and restart the editor. For a
project outside the demo host, install the companion `LevelGenPCG` plugin next
to `LevelGen` in the project's Plugins folder. Enabling the companion also
enables Unreal's **Procedural Content Generation Framework**. Projects that
only use the LevelGen actor can use the main plugin on its own.

Add **Generate LevelGen Points** to a PCG graph. Set **Layout Seed**, **Layout
Template**, **Width**, **Height**, and **Cell Size Mm** in the node details,
or drive them with PCG attribute overrides. A size of zero selects the template
default. Compact Vertical uses a 24 x 24 grid and supports 3 to 5 floors.
Elevator Shaft supports 2 to 16 floors. Set **Floor Height Cm** to change
vertical spacing. Assign a **Theme** to emit themed props. Compact Vertical
also emits its built-in vertical dressing anchors.

| Pin | Placement |
| --- | --- |
| Floors | Walkable tile centres, with shaft and stair openings preserved |
| Walls | Solid tile centres, including buried solids |
| Doors | Room/corridor edge centres, with local +X normal to the opening |
| Props | Rotated theme footprint centres and Compact Vertical dressing anchors |

Each dataset carries `CellTags` (integer bitmask from the LevelGen cell-tag
contract), `Tier` (integer, 0 core, 1 detail, 2 clutter, -1 for structural
points), `PropId` (string, empty for structural points), and `FloorIndex`
(zero-based integer). Walls use the solid cell's zero mask and doors combine
the masks of the two adjoining cells. Transforms are in world space relative
to the original PCG component. Use the output pins with PCG filters and mesh
spawners. The graph supplies meshes, materials and any additional components.

The demo graph is `/Game/LevelGenDemo/PCG_LevelGenDemo`. It uses seed 7 with
Compact Vertical and forwards all four streams to named graph outputs. In a
fresh source checkout, the `LevelGen.PCG.SampleGraph` editor automation check
creates and saves the asset if it is missing. Run it from Session Frontend
under **Automation** after building the demo host, then assign the graph to a
PCG component to inspect its points.
