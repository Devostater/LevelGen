"""Create the LevelGen demo assets in the host project from the editor."""

import sys

import unreal


DEMO_DIR = "/Game/LevelGenDemo"
MAP_PATH = f"{DEMO_DIR}/LevelGenDemo"
VERTICAL_MAP_PATH = f"{DEMO_DIR}/LevelGenDemo_Vertical"
HUB_MAP_PATH = f"{DEMO_DIR}/LevelGenDemo_HubAndWings"
ROOM_MAP_PATH = f"{DEMO_DIR}/LevelGenRoomTemplate"
THEME_NAME = "BasicShapesTheme"
THEME_PATH = f"{DEMO_DIR}/{THEME_NAME}"


def load_shape(name):
    mesh = unreal.load_asset(f"/Engine/BasicShapes/{name}.{name}")
    if not isinstance(mesh, unreal.StaticMesh):
        raise RuntimeError(f"Could not load engine mesh {name}.")
    return mesh


def make_prop(prop_id, mesh, tier, tags, density, max_per_room, interactable=None):
    prop = unreal.LevelGenProp()
    properties = {
        "id": prop_id,
        "mesh": mesh,
        "tier": tier,
        "allowed_tags": tags,
        "density": density,
        "max_per_room": max_per_room,
        "rotations": [0, 90, 180, 270],
    }
    for name, value in properties.items():
        prop.set_editor_property(name, value)
    if interactable is not None:
        prop.set_editor_property("interactable_class", interactable.static_class())
    return prop


def create_demo():
    levels = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if levels.is_in_play_in_editor():
        unreal.log_warning("Stop Play in Editor before creating the LevelGen demo.")
        return
    assets = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    if registry.get_assets_by_package_name(MAP_PATH):
        unreal.log(f"Demo already exists. Open {MAP_PATH} in the Content Browser.")
        return

    cube = load_shape("Cube")
    cylinder = load_shape("Cylinder")
    plane = load_shape("Plane")

    theme = assets.load_asset(THEME_PATH) if assets.does_asset_exist(THEME_PATH) else None
    if theme is None:
        factory = unreal.DataAssetFactory()
        factory.set_editor_property("data_asset_class", unreal.LevelGenTheme.static_class())
        theme = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            THEME_NAME, DEMO_DIR, unreal.LevelGenTheme.static_class(), factory
        )
        if theme is None:
            raise RuntimeError("Could not create the LevelGen demo theme.")
        wall_edge, corner, center = 1, 2, 4
        theme.set_editor_property("props", [
            make_prop("drum", cylinder, unreal.LevelGenPropTier.CORE, wall_edge, 10000, 2),
            make_prop("crate", cube, unreal.LevelGenPropTier.DETAIL, corner, 10000, 2),
            make_prop("spare-drum", cylinder, unreal.LevelGenPropTier.CLUTTER,
                      wall_edge | center, 10000, 4, unreal.LevelGenPickup),
        ])
        if not assets.save_loaded_asset(theme):
            raise RuntimeError("Could not save the LevelGen demo theme.")

    if not levels.new_level(MAP_PATH):
        raise RuntimeError("Could not create the LevelGen demo map.")
    generator = actors.spawn_actor_from_class(unreal.LevelGenActor, unreal.Vector())
    if generator is None:
        raise RuntimeError("Could not place the LevelGen Actor.")
    generator.set_actor_label("LevelGen Demo Generator")
    generator.set_editor_properties({
        "seed": 42,
        "preset": unreal.LevelGenPreset.SMALL,
        "cell_size": 1000,
        "floor_mesh": plane,
        "wall_mesh": cube,
        "theme": theme,
        "quality": unreal.LevelGenQuality.ULTRA,
        "enable_interactables": True,
        "enable_story": False,
        "potato_room_distance": 600.0,
    })
    if not generator.generate():
        raise RuntimeError("LevelGen could not generate the demo. See the Output Log.")

    sun = actors.spawn_actor_from_class(
        unreal.DirectionalLight, unreal.Vector(), unreal.Rotator(pitch=-55, yaw=-35)
    )
    sun.get_editor_property("light_component").set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
    # Cell (4, 6) is the start for seed 42. Face the corridor at a height
    # where the default flying pawn clears the floor and still hits the walls.
    actors.spawn_actor_from_class(
        unreal.PlayerStart, unreal.Vector(450, 650, 60), unreal.Rotator(pitch=-10)
    )
    actors.set_selected_level_actors([generator])
    unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).set_level_viewport_camera_info(
        unreal.Vector(100, 800, 2200), unreal.Rotator(pitch=-62)
    )
    if not levels.save_current_level():
        raise RuntimeError("Could not save the generated LevelGen demo map.")
    unreal.log(f"Created {MAP_PATH} and {THEME_PATH}.")


def create_hub_demo():
    levels = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if levels.is_in_play_in_editor():
        raise RuntimeError("Stop Play in Editor before creating the Hub and Wings demo.")

    assets = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    if not registry.get_assets_by_package_name(ROOM_MAP_PATH):
        if not levels.new_level(ROOM_MAP_PATH) or not levels.save_current_level():
            raise RuntimeError("Could not save the empty room streaming template.")

    if not registry.get_assets_by_package_name(HUB_MAP_PATH):
        theme = assets.load_asset(THEME_PATH)
        if theme is None:
            raise RuntimeError("Create the basic demo and BasicShapesTheme first.")
        if not levels.new_level(HUB_MAP_PATH):
            raise RuntimeError("Could not create the Hub and Wings demo map.")
        room_template = unreal.load_object(None, f"{ROOM_MAP_PATH}.LevelGenRoomTemplate")
        if room_template is None:
            raise RuntimeError("Could not load the empty room streaming template.")

        # One-metre cells match the basic-shape meshes. The seed-7 entrance is cell (22, 7).
        appearance = {
            "seed": 7,
            "cell_size": 1000,
            "floor_mesh": load_shape("Plane"),
            "wall_mesh": load_shape("Cube"),
        }
        hub = actors.spawn_actor_from_class(unreal.LevelGenActor, unreal.Vector())
        hub.set_actor_label("Hub and Wings Generator")
        hub.set_editor_properties({
            **appearance,
            "preset": unreal.LevelGenPreset.HUB_AND_WINGS,
            "theme": theme,
            "stream_rooms": True,
            "room_level_template": room_template,
            "room_load_radius": 750.0,
        })
        if not hub.generate():
            raise RuntimeError("Could not generate Hub and Wings. See the Output Log.")

        # The elevator has its own grid beside the hub. Its landing is at local cell (11, 7).
        elevator = actors.spawn_actor_from_class(unreal.LevelGenActor, unreal.Vector(-2900, 0, 0))
        elevator.set_actor_label("Three-Stop Elevator Sample")
        elevator.set_editor_properties({
            **appearance,
            "preset": unreal.LevelGenPreset.ELEVATOR_SHAFT,
            "elevator_stops": 3,
        })
        if not elevator.generate():
            raise RuntimeError("Could not generate the elevator sample. See the Output Log.")

        sun = actors.spawn_actor_from_class(
            unreal.DirectionalLight, unreal.Vector(), unreal.Rotator(pitch=-55, yaw=-35)
        )
        sun.get_editor_property("light_component").set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
        actors.spawn_actor_from_class(
            unreal.PlayerStart, unreal.Vector(2250, 750, 65), unreal.Rotator(yaw=90)
        )
        actors.set_selected_level_actors([hub])
        if not levels.save_current_level():
            raise RuntimeError("Could not save the Hub and Wings demo map.")

    if not levels.load_level(HUB_MAP_PATH):
        raise RuntimeError("Could not reopen the Hub and Wings demo map.")
    generators = {
        actor.get_actor_label(): actor
        for actor in actors.get_all_level_actors() if isinstance(actor, unreal.LevelGenActor)
    }
    hub = generators["Hub and Wings Generator"]
    elevator = generators["Three-Stop Elevator Sample"]
    if (hub.get_editor_property("seed") != 7
            or hub.get_editor_property("preset") != unreal.LevelGenPreset.HUB_AND_WINGS
            or not hub.get_editor_property("stream_rooms")
            or hub.get_editor_property("room_level_template").get_path_name().split(".")[0] != ROOM_MAP_PATH
            or elevator.get_editor_property("preset") != unreal.LevelGenPreset.ELEVATOR_SHAFT
            or elevator.get_editor_property("elevator_stops") != 3):
        raise RuntimeError("The saved Hub and Wings demo has unexpected generator settings.")
    for generator in (hub, elevator):
        meshes = generator.get_components_by_class(unreal.InstancedStaticMeshComponent)
        if not any(mesh.get_instance_count() for mesh in meshes):
            raise RuntimeError(f"The saved preview is empty for {generator.get_actor_label()}.")
    unreal.log("LevelGen Hub and Wings demo verified.")


def create_vertical_demo():
    levels = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    if levels.is_in_play_in_editor():
        raise RuntimeError("Stop Play in Editor before creating the Compact Vertical demo.")

    if not registry.get_assets_by_package_name(ROOM_MAP_PATH):
        if not levels.new_level(ROOM_MAP_PATH) or not levels.save_current_level():
            raise RuntimeError("Could not save the empty floor streaming template.")
    room_template = unreal.load_object(None, f"{ROOM_MAP_PATH}.LevelGenRoomTemplate")
    if room_template is None:
        raise RuntimeError("Could not load the empty floor streaming template.")

    if registry.get_assets_by_package_name(VERTICAL_MAP_PATH):
        if not levels.load_level(VERTICAL_MAP_PATH):
            raise RuntimeError("Could not load the Compact Vertical demo map.")
    elif not levels.new_level(VERTICAL_MAP_PATH):
        raise RuntimeError("Could not create the Compact Vertical demo map.")

    if not any(isinstance(actor, unreal.LevelGenActor) for actor in actors.get_all_level_actors()):
        generator = actors.spawn_actor_from_class(unreal.LevelGenActor, unreal.Vector())
        generator.set_actor_label("Compact Vertical Generator")
        generator.set_editor_properties({
            "seed": 42,
            "preset": unreal.LevelGenPreset.COMPACT_VERTICAL,
            "compact_floors": 4,
            "elevator_floor_height": 300.0,
            "cell_size": 1000,
            "floor_mesh": load_shape("Plane"),
            "wall_mesh": load_shape("Cube"),
            "quality": unreal.LevelGenQuality.ULTRA,
            "stream_rooms": True,
            "room_level_template": room_template,
            "room_load_radius": 500.0,
        })
        if not generator.generate():
            raise RuntimeError("Could not generate Compact Vertical. See the Output Log.")

        sun = actors.spawn_actor_from_class(
            unreal.DirectionalLight, unreal.Vector(), unreal.Rotator(pitch=-55, yaw=-35)
        )
        sun.get_editor_property("light_component").set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
        actors.spawn_actor_from_class(
            unreal.PlayerStart, unreal.Vector(350, 1950, 65), unreal.Rotator(yaw=-90)
        )
        actors.set_selected_level_actors([generator])
        unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).set_level_viewport_camera_info(
            unreal.Vector(-1400, 1200, 2400), unreal.Rotator(pitch=-30)
        )
        if not levels.save_current_level():
            raise RuntimeError("Could not save the Compact Vertical demo map.")

    if not levels.load_level(VERTICAL_MAP_PATH):
        raise RuntimeError("Could not reopen the Compact Vertical demo map.")
    generators = [actor for actor in actors.get_all_level_actors() if isinstance(actor, unreal.LevelGenActor)]
    if len(generators) != 1:
        raise RuntimeError("Expected one generator in the saved Compact Vertical demo.")
    generator = generators[0]
    if (generator.get_editor_property("preset") != unreal.LevelGenPreset.COMPACT_VERTICAL
            or generator.get_editor_property("compact_floors") != 4
            or not generator.get_editor_property("stream_rooms")
            or list(generator.get_editor_property("floor_roles")) != ["arrival", "service", "overlook", "finale"]):
        raise RuntimeError("The saved Compact Vertical demo has unexpected generator settings.")
    def instance_count():
        return sum(mesh.get_instance_count() for mesh in
                   generator.get_components_by_class(unreal.InstancedStaticMeshComponent))

    ultra = instance_count()
    generator.set_quality(unreal.LevelGenQuality.HIGH)
    high = instance_count()
    generator.set_quality(unreal.LevelGenQuality.POTATO)
    potato = instance_count()
    generator.set_quality(unreal.LevelGenQuality.ULTRA)
    if not 0 < potato < high < ultra or instance_count() != ultra:
        raise RuntimeError("The saved Compact Vertical preview failed the quality switch check.")
    unreal.log("LevelGen Compact Vertical demo verified.")


if __name__ == "__main__":
    if "--vertical" in sys.argv:
        create_vertical_demo()
    elif "--hub" in sys.argv:
        create_hub_demo()
    else:
        create_demo()
