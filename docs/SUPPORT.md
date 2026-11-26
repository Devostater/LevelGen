# LevelGen support

## Quick start

1. In Unreal Engine 5.8 on Windows, enable **LevelGen** from **Edit > Plugins**. Restart the editor if prompted.
2. Open the map you want to generate into, then choose **Window > LevelGen** or click the LevelGen toolbar icon.
3. Click **Generate level** or press **Ctrl+Shift+G**. On an empty map, accept the prompt to add a generator. The panel reports the room count, floor count, and time.
4. Try a preset card or adjust **Size**, **Floors**, **Loot and pickups**, **Lighting mood**, and **Theme**. Turn on **Live preview** to see each floor as you make changes. Enter and lock a seed to repeat a layout. Open **Details** for advanced options.
5. Click **Export minimap PNG** to save the current generation to `Saved/Minimaps/Minimap.png` by default. Stacked levels get numbered files in floor order. Click **Bake to level** when you want editable actors, then save the map. Export before baking if you want a minimap of that generation.

The panel remembers its welcome dismissal, seed lock, live preview, and defaults for new generators in this project. Save the map to keep settings on its generator. Use **Save current as preset** to share a set of settings as an asset.

## Common questions

1. **Why is the preview empty?** Turn on **Live preview**. If generation also fails on an existing generator, check its floor and wall meshes and look for the first LevelGen error in the Output Log.
2. **Why do the walls or floors look offset?** Use cell-centred pivots. Put the floor's walkable surface at pivot height. **Cell Size** uses millimetres and **Wall Height** uses centimetres.
3. **How do I rebuild the same layout?** Keep the seed, layout preset, and generation settings the same. Keep the theme and assets the same to match the dressing and visuals.
4. **How do I enable streaming?** Assign an empty, non-partitioned map to **Room Level Template**, enable **Stream Rooms**, and regenerate. Use `stat levels` during single-player play to inspect loaded chunks.
5. **How do I get matching multiplayer layouts?** Enable **Replicates** on the actor, assign shared cooked assets, and call **Generate** on the server. Clients build from the replicated inputs. Multiplayer uses the full layout, and your game handles shared gameplay state.
6. **How do I change the minimap destination or resolution?** Set **Minimap PNG Path** and **Minimap Pixels Per Cell** in **Details > Layout**, then generate and export. For Blueprint use, see the [minimap guide](USER_GUIDE.md#minimap-export).
7. **How do I add props and lights?** Assign a **Level Gen Theme** data asset with your prop meshes. Enable **Auto Lights** and use **Room Lights** in the theme to customize lighting.
8. **Where is the PCG sample?** Open the separate demo host. Enable **LevelGen PCG**, restart the editor, and look for `/Game/LevelGenDemo/PCG_LevelGenDemo`. [PCG setup](USER_GUIDE.md#pcg-graphs)

## Report a bug

Use the support contact on the LevelGen Fab listing. Include your UE patch version, LevelGen version, Windows version, seed, preset and changed settings. Give the shortest steps to reproduce it, what you expected, and what happened. Attach the relevant Output Log excerpt and a screenshot if it helps. For a multiplayer mismatch, include the host and client results and say whether the client joined late.