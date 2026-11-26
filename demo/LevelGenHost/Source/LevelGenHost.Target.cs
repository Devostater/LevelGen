using UnrealBuildTool;

public class LevelGenHostTarget : TargetRules
{
    public LevelGenHostTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("LevelGenHost");
    }
}
