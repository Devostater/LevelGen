using UnrealBuildTool;

public class LevelGenHost : ModuleRules
{
    public LevelGenHost(ReadOnlyTargetRules Target) : base(Target)
    {
        PrivateDependencyModuleNames.AddRange(new[] { "Core", "CoreUObject", "Engine", "InputCore", "LevelGen" });
    }
}
