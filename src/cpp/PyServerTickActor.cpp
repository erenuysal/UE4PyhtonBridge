// Fill out your copyright notice in the Description page of Project Settings.

#include "PyServerTickActor.h"
#include "PyServerPrivatePCH.h"
#include "Engine.h"
#include "PythonProxy.h"
#include <stdio.h>

// Sets default values
APyServerTickActor::APyServerTickActor()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;
	UE_LOG(LogTemp, Warning, TEXT("Init APyServerTickActor\n"));
//	LoadPythonInterperter();
}

// Called when the game starts or when spawned
void APyServerTickActor::BeginPlay()
{
	Super::BeginPlay();
	UE_LOG(LogTemp, Warning, TEXT("called APyServerTickActor::BeginPlay\n"));
//	mybeginplay();	
}

void APyServerTickActor::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	Super::EndPlay(EndPlayReason);
	UE_LOG(LogTemp, Warning, TEXT("called APyServerTickActor::EndPlay\n"));
//	myendplay();	
}


// Called every frame
void APyServerTickActor::Tick( float DeltaTime )
{
	Super::Tick( DeltaTime );
//	mytick();	

}

