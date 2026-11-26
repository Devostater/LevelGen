#include "LevelGenDemoGameMode.h"

#include "Components/InputComponent.h"
#include "Engine/World.h"
#include "GameFramework/Pawn.h"
#include "InputCoreTypes.h"
#include "LevelGenElevator.h"
#include "LevelGenActor.h"
#include "EngineUtils.h"

ALevelGenDemoGameMode::ALevelGenDemoGameMode()
{
    PlayerControllerClass = ALevelGenDemoPlayerController::StaticClass();
}

void ALevelGenDemoPlayerController::SetupInputComponent()
{
    Super::SetupInputComponent();
    InputComponent->BindKey(EKeys::E, IE_Pressed, this, &ALevelGenDemoPlayerController::UseElevatorButton);
    InputComponent->BindKey(EKeys::Q, IE_Pressed, this, &ALevelGenDemoPlayerController::DescendLadder);
}

void ALevelGenDemoPlayerController::UseElevatorButton()
{
    FVector Eye;
    FRotator View;
    GetPlayerViewPoint(Eye, View);
    FHitResult Hit;
    FCollisionQueryParams Query;
    if (const APawn* ControlledPawn = GetPawn())
    {
        Query.AddIgnoredActor(ControlledPawn);
    }

    if (GetWorld()->LineTraceSingleByChannel(Hit, Eye, Eye + View.Vector() * 250.0, ECC_Visibility, Query))
    {
        if (ALevelGenElevatorButton* Button = Cast<ALevelGenElevatorButton>(Hit.GetActor()))
        {
            Button->Interact();
            return;
        }
    }
    UseLadder(true);
}

void ALevelGenDemoPlayerController::DescendLadder()
{
    UseLadder(false);
}

void ALevelGenDemoPlayerController::UseLadder(bool bUp)
{
    if (!GetPawn()) return;
    for (TActorIterator<ALevelGenActor> It(GetWorld()); It; ++It)
    {
        if (It->UseVerticalLadder(GetPawn(), bUp)) return;
    }
}
