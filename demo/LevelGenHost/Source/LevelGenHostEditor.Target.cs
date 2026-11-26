using UnrealBuildTool;

public class LevelGenHostEditorTarget : TargetRules
{
    public LevelGenHostEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("LevelGenHost");
    }
}
