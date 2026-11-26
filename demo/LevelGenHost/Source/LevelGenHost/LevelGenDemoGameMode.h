#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "GameFramework/PlayerController.h"
#include "LevelGenDemoGameMode.generated.h"

UCLASS()
class ALevelGenDemoPlayerController : public APlayerController
{
    GENERATED_BODY()

protected:
    void SetupInputComponent() override;

private:
    void UseElevatorButton();
    void DescendLadder();
    void UseLadder(bool bUp);
};

UCLASS()
class ALevelGenDemoGameMode : public AGameModeBase
{
    GENERATED_BODY()

public:
    ALevelGenDemoGameMode();
};
