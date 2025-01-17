from logic.helpers import Bosses
from utils.parameters import Settings
from rom.rom_patches import RomPatches
from logic.smbool import SMBool
from graph.location import locationsDict, LocationMapAttrs, LocationMapTileKind
from rom.addresses import Addresses

loc = locationsDict["Energy Tank, Gauntlet"]
loc.AccessFrom = {
    'Landing Site': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wor(sm.canEnterAndLeaveGauntlet(),
                      sm.wand(sm.canShortCharge(),
                              sm.canEnterAndLeaveGauntletQty(1, 0)), # thanks ponk! https://youtu.be/jil5zTBCF1s
                      sm.canDoLowGauntlet())
)


loc = locationsDict["Bomb"]
loc.AccessFrom = {
    'Landing Site': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.haveItem('Morph'),
                       sm.traverse('FlywayRight'))
)
loc.PostAvailable = (
    lambda sm: sm.wor(sm.knowsAlcatrazEscape(),
                      sm.canPassBombPassages())
)


loc = locationsDict["Energy Tank, Terminator"]
loc.AccessFrom = {
    'Landing Site': lambda sm: sm.canPassTerminatorBombWall(),
    'Lower Mushrooms Left': lambda sm: sm.canPassCrateriaGreenPirates(),
    'Gauntlet Top': lambda sm: sm.haveItem('Morph')
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Reserve Tank, Brinstar"]
loc.AccessFrom = {
    'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
}
loc.Available = (
    lambda sm: sm.wand(sm.wor(sm.canMockball(),
                              sm.haveItem('SpeedBooster')),
                       sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('EarlySupersRight')))
)


loc = locationsDict["Charge Beam"]
loc.AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.canPassBombPassages()
)


loc = locationsDict["Morphing Ball"]
loc.AccessFrom = {
    'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Energy Tank, Brinstar Ceiling"]
loc.AccessFrom = {
    'Blue Brinstar Elevator Bottom': lambda sm: sm.wor(RomPatches.has(RomPatches.BlueBrinstarBlueDoor), sm.traverse('ConstructionZoneRight'))
}
loc.Available = (
    lambda sm: sm.wor(sm.knowsCeilingDBoost(),
                      sm.canFly(),
                      sm.wor(sm.haveItem('HiJump'),
                             sm.haveItem('Ice'),
                             sm.wand(sm.canUsePowerBombs(),
                                     sm.haveItem('SpeedBooster')),
                             sm.canSimpleShortCharge()))
)


loc = locationsDict["Energy Tank, Etecoons"]
loc.AccessFrom = {
    'Etecoons Bottom': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Energy Tank, Waterway"]
loc.AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.canUsePowerBombs(),
                       sm.traverse('BigPinkBottomLeft'),
                       sm.haveItem('SpeedBooster'),
                       sm.wor(sm.haveItem('Gravity'),
                              sm.canSimpleShortCharge())) # from the blocks above the water
)


loc = locationsDict["Energy Tank, Brinstar Gate"]
loc.AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.traverse('BigPinkRight'),
                       sm.wor(sm.haveItem('Wave'),
                              sm.wand(sm.haveItem('Super'),
                                      sm.haveItem('HiJump'),
                                      sm.knowsReverseGateGlitch()),
                              sm.wand(sm.haveItem('Super'),
                                      sm.knowsReverseGateGlitchHiJumpLess())))
)


loc = locationsDict["X-Ray Scope"]
loc.AccessFrom = {
    'Red Tower Top Left': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.canUsePowerBombs(),
                       sm.traverse('RedTowerLeft'),
                       sm.traverse('RedBrinstarFirefleaLeft'),
                       sm.wor(sm.haveItem('Grapple'),
                              sm.haveItem('SpaceJump'),
                              sm.wand(sm.energyReserveCountOkHardRoom('X-Ray'),
                                      sm.wor(sm.knowsXrayDboost(),
                                             sm.wand(sm.haveItem('Ice'),
                                                     sm.wor(sm.haveItem('HiJump'), sm.knowsXrayIce())),
                                             sm.canInfiniteBombJump(),
                                             sm.wand(sm.haveItem('HiJump'),
                                                     sm.wor(sm.haveItem('SpeedBooster'),
                                                            sm.canSpringBallJump()))))))
)


loc = locationsDict["Spazer"]
loc.AccessFrom = {
    'East Tunnel Right': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.traverse('BelowSpazerTopRight'),
                       sm.wor(sm.canPassBombPassages(),
                              sm.wand(sm.haveItem('Morph'),
                                      RomPatches.has(RomPatches.SpazerShotBlock))))
)


loc = locationsDict["Energy Tank, Kraid"]
loc.AccessFrom = {
    'Warehouse Zeela Room Left': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(Bosses.bossDead(sm, 'Kraid'),
                       # kill the beetoms to unlock the door to get out
                       sm.canKillBeetoms())
)


loc = locationsDict["Kraid"]
loc.AccessFrom = {
    'KraidRoomIn': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.enoughStuffsKraid()
)


loc = locationsDict["Varia Suit"]
loc.AccessFrom = {
    'KraidRoomIn': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: Bosses.bossDead(sm, 'Kraid')
)


loc = locationsDict["Ice Beam"]
loc.AccessFrom = {
    'Business Center': lambda sm: sm.traverse('BusinessCenterTopLeft')
}
loc.Available = (
    lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['Ice']['Norfair Entrance -> Ice Beam']),
                       sm.wor(sm.canPassBombPassages(), # to exit, or if you fail entrance
                              sm.wand(sm.haveItem('Ice'), # harder strat
                                      sm.haveItem('Morph'),
                                      sm.knowsIceEscape())),
                       sm.wor(sm.wand(sm.haveItem('Morph'),
                                      sm.knowsMockball()),
                              sm.haveItem('SpeedBooster')))
)


loc = locationsDict["Energy Tank, Crocomire"]
loc.AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.haveItem('Crocomire'),
                       sm.wor(sm.haveItem('Grapple'),
                              sm.haveItem('SpaceJump'),
                              sm.energyReserveCountOk(3/sm.getDmgReduction()[0])))
)


loc = locationsDict["Hi-Jump Boots"]
loc.AccessFrom = {
    'Business Center': lambda sm: sm.wor(RomPatches.has(RomPatches.HiJumpAreaBlueDoor), sm.traverse('BusinessCenterBottomLeft'))
}
loc.Available = (
    lambda sm: sm.haveItem('Morph')
)
loc.PostAvailable = (
    lambda sm: sm.wor(sm.canPassBombPassages(),
                      sm.wand(sm.haveItem('Morph'), RomPatches.has(RomPatches.HiJumpShotBlock)))
)


loc = locationsDict["Grapple Beam"]
loc.AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.haveItem('Crocomire'),
                       sm.wor(sm.wand(sm.haveItem('Morph'),
                                      sm.canFly()),
                              sm.wand(sm.haveItem('SpeedBooster'),
                                      sm.wor(sm.knowsShortCharge(),
                                             sm.canUsePowerBombs())),
                              sm.wand(sm.haveItem('Morph'),
                                      sm.wor(sm.haveItem('SpeedBooster'),
                                             sm.canSpringBallJump()),
                                      sm.haveItem('HiJump')), # jump from the yellow plateform ennemy
                              sm.canGreenGateGlitch()))
)
loc.PostAvailable = (
    lambda sm: sm.wor(sm.haveItem('Morph'), # regular exit
                      sm.wand(sm.haveItem('Super'), # grapple escape reverse
                              sm.wor(sm.canFly(), # Grapple Tutorial Room 2
                                     sm.haveItem('HiJump'),
                                     sm.haveItem('Grapple')),
                              sm.wor(sm.haveItem('Gravity'), # Grapple Tutorial Room 3
                                     sm.haveItem('SpaceJump'),
                                     sm.haveItem('Grapple'))))
)


loc = locationsDict["Reserve Tank, Norfair"]
loc.AccessFrom = {
    'Bubble Mountain': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutain(),
    'Bubble Mountain Top': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutainTop(),
}
loc.Available = (
    lambda sm: sm.wand(sm.haveItem('Morph'), sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Norfair Reserve']))
)


loc = locationsDict["Speed Booster"]
loc.AccessFrom = {
    'Bubble Mountain Top': lambda sm: sm.wor(RomPatches.has(RomPatches.SpeedAreaBlueDoors),
                                             sm.wand(sm.traverse('BubbleMountainTopRight'),
                                                     sm.traverse('SpeedBoosterHallRight')))
}
loc.Available = (
    lambda sm: sm.canHellRunToSpeedBooster()
)


loc = locationsDict["Wave Beam"]
loc.AccessFrom = {
    'Bubble Mountain Top': lambda sm: sm.canAccessDoubleChamberItems()
}
loc.Available = (
    lambda sm: sm.traverse('DoubleChamberRight')
)
loc.PostAvailable = (
    lambda sm: sm.canExitWaveBeam()
)


loc = locationsDict["Ridley"]
loc.AccessFrom = {
    'RidleyRoomIn': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']), sm.enoughStuffsRidley())
)


loc = locationsDict["Energy Tank, Ridley"]
loc.AccessFrom = {
    'RidleyRoomIn': lambda sm: sm.wand(sm.haveItem('Ridley'), sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']))
}
loc.Available = (
    lambda sm: sm.haveItem('Morph')
)


loc = locationsDict["Screw Attack"]
loc.AccessFrom = {
    'Screw Attack Bottom': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)
loc.PostAvailable = (
    lambda sm: sm.canExitScrewAttackArea()
)


loc = locationsDict["Energy Tank, Firefleas"]
loc.AccessFrom = {
    'Firefleas': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wor(RomPatches.has(RomPatches.FirefleasRemoveFune),
                      # get past the fune
                                     sm.haveItem('Super'),
                      sm.canPassBombPassages(),
                      sm.canUseSpringBall())
)
loc.PostAvailable = (
    lambda sm: sm.wor(sm.knowsFirefleasWalljump(),
                      sm.wor(sm.haveItem('Ice'),
                             sm.haveItem('HiJump'),
                             sm.canFly(),
                             sm.canSpringBallJump()))
)


loc = locationsDict["Reserve Tank, Wrecked Ship"]
loc.AccessFrom = {
    'Bowling': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.canUsePowerBombs(),
                       sm.haveItem('SpeedBooster'))
)


loc = locationsDict["Energy Tank, Wrecked Ship"]
loc.AccessFrom = {
    'Wrecked Ship Back': lambda sm: sm.wor(RomPatches.has(RomPatches.WsEtankBlueDoor),
                                           sm.traverse('ElectricDeathRoomTopLeft'))
}
loc.Available = (
    lambda sm: sm.wor(Bosses.bossDead(sm, 'Phantoon'),
                      RomPatches.has(RomPatches.WsEtankPhantoonAlive))
)


loc = locationsDict["Phantoon"]
loc.AccessFrom = {
    'PhantoonRoomIn': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.enoughStuffsPhantoon()
)


loc = locationsDict["Right Super, Wrecked Ship"]
loc.AccessFrom = {
    'Wrecked Ship Main': lambda sm: Bosses.bossDead(sm, 'Phantoon')
}
loc.Available = (
    lambda sm: sm.canPassBombPassages()
)


loc = locationsDict["Gravity Suit"]
loc.AccessFrom = {
    'Bowling': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Energy Tank, Mama turtle"]
loc.AccessFrom = {
    'Main Street Bottom': lambda sm: sm.wand(sm.canDoOuterMaridia(),
                                             sm.wor(sm.traverse('FishTankRight'),
                                                    RomPatches.has(RomPatches.MamaTurtleBlueDoor)),
                                             sm.wor(sm.wand(sm.haveItem('Gravity'),
                                                            sm.haveItem('SpeedBooster')),
                                                    sm.haveItem('Grapple'),
                                                    sm.canFly(),
                                                    sm.wand(sm.haveItem('HiJump'),
                                                            sm.haveItem('SpeedBooster'),
                                                            sm.knowsHiJumpMamaTurtle()),
                                                    sm.wand(sm.canUseSpringBall(),
                                                            sm.wor(sm.wand(sm.haveItem('HiJump'),
                                                                           sm.knowsSpringBallJump()),
                                                                   sm.knowsSpringBallJumpFromWall())),
                                                    sm.wand(sm.canPassBombPassages(),
                                                            sm.knowsMamaTurtleWallJumpBombBoost()))),
    'Mama Turtle': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Plasma Beam"]
loc.AccessFrom = {
    'Toilet Top': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: Bosses.bossDead(sm, 'Draygon')
)
loc.PostAvailable = (
    lambda sm: sm.wand(sm.wor(sm.wand(sm.canShortCharge(),
                                      sm.knowsKillPlasmaPiratesWithSpark()),
                              sm.wand(sm.canFireChargedShots(),
                                      sm.knowsKillPlasmaPiratesWithCharge(),
                                      # 160/80/40 dmg * 4 ground plasma pirates
                                      # => 640/320/160 damage take required
                                      # check below is 1099/599/299 (give margin for taking dmg a bit)
                                      # (* 4 for nerfed charge, since you need to take hits 4 times instead of one)
                                                       sm.energyReserveCountOk(int(10.0 * sm.getPiratesPseudoScrewCoeff()/sm.getDmgReduction(False)[0]))),
                              sm.haveItem('ScrewAttack'),
                              sm.haveItem('Plasma')),
                       sm.wor(sm.canFly(),
                              sm.wand(sm.haveItem('HiJump'),
                                      sm.knowsGetAroundWallJump()),
                              sm.canShortCharge(),
                              sm.wand(sm.canSpringBallJump(),
                                      sm.knowsSpringBallJumpFromWall())))
)


loc = locationsDict["Reserve Tank, Maridia"]
loc.AccessFrom = {
    'Left Sandpit': lambda sm: sm.canClimbWestSandHole()
}
loc.Available = (
    lambda sm: sm.canAccessItemsInWestSandHole()
)


loc = locationsDict["Spring Ball"]
loc.AccessFrom = {
    'Oasis Bottom': lambda sm: sm.canTraverseSandPits()
}
loc.Available = (
    lambda sm: sm.wand(sm.canAccessShaktoolFromPantsRoom(),
                       sm.canUsePowerBombs(), # in Shaktool room to let Shaktool access the sand blocks
                       sm.wor(sm.haveItem('Gravity'), sm.canUseSpringBall())) # acess the item in spring ball room
)
loc.PostAvailable = (
    lambda sm: sm.wor(sm.wand(sm.haveItem('Gravity'),
                              sm.wor(sm.haveItem('HiJump'),
                                     sm.canFly(),
                                     sm.knowsMaridiaWallJumps())),
                      sm.canSpringBallJump())
)


loc = locationsDict["Energy Tank, Botwoon"]
loc.AccessFrom = {
    'Post Botwoon': lambda sm: sm.canJumpUnderwater()
}
loc.Available = (
    lambda sm: sm.haveItem('Morph')
)


loc = locationsDict["Draygon"]
loc.AccessFrom = {
    'Draygon Room Bottom': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Space Jump"]
loc.AccessFrom = {
    'Draygon Room Bottom': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)
loc.PostAvailable = (
    lambda sm: Bosses.bossDead(sm, 'Draygon')
)


loc = locationsDict["Mother Brain"]
loc.AccessFrom = {
    'Golden Four': lambda sm: sm.canPassG4()
}
loc.Available = (
    lambda sm: sm.wor(RomPatches.has(RomPatches.NoTourian),
                      sm.enoughStuffTourian())
)


loc = locationsDict["Spore Spawn"]
loc.AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.traverse('BigPinkTopRight'),
                       sm.enoughStuffSporeSpawn())
)


loc = locationsDict["Botwoon"]
loc.AccessFrom = {
    'Aqueduct Bottom': lambda sm: sm.canJumpUnderwater()
}
loc.Available = (
    # includes botwoon hallway conditions
    lambda sm: sm.canDefeatBotwoon()
)


loc = locationsDict["Crocomire"]
loc.AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.enoughStuffCroc()
)


loc = locationsDict["Golden Torizo"]
loc.AccessFrom = {
    'Screw Attack Bottom': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.enoughStuffGT()
)


loc = locationsDict["Power Bomb (Crateria surface)"]
loc.AccessFrom = {
    'Landing Site': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.traverse('LandingSiteTopRight'),
                       sm.wor(sm.haveItem('SpeedBooster'),
                              sm.canFly()))
)


loc = locationsDict["Missile (outside Wrecked Ship bottom)"]
loc.AccessFrom = {
    'West Ocean Left': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.haveItem('Morph')
)
loc.PostAvailable = (
    lambda sm: sm.canPassBombPassages()
)


loc = locationsDict["Missile (outside Wrecked Ship top)"]
loc.AccessFrom = {
    'Wrecked Ship Main': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: Bosses.bossDead(sm, 'Phantoon')
)


loc = locationsDict["Missile (outside Wrecked Ship middle)"]
loc.AccessFrom = {
    'Wrecked Ship Main': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.haveItem('Super'), sm.haveItem('Morph'), Bosses.bossDead(sm, 'Phantoon'))
)


loc = locationsDict["Missile (Crateria moat)"]
loc.AccessFrom = {
    'Moat Left': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Missile (Crateria bottom)"]
loc.AccessFrom = {
    'Landing Site': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wor(sm.canDestroyBombWalls(),
                      sm.wand(sm.haveItem('SpeedBooster'),
                              sm.knowsOldMBWithSpeed()))
)


loc = locationsDict["Missile (Crateria gauntlet right)"]
loc.AccessFrom = {
    'Landing Site': lambda sm: sm.wor(sm.wand(sm.canEnterAndLeaveGauntlet(),
                                              sm.canPassBombPassages()),
                                      sm.canDoLowGauntlet()),
    'Gauntlet Top': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Missile (Crateria gauntlet left)"]
loc.AccessFrom = {
    'Landing Site': lambda sm: sm.wor(sm.wand(sm.canEnterAndLeaveGauntlet(),
                                              sm.canPassBombPassages()),
                                      sm.canDoLowGauntlet()),
    'Gauntlet Top': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Super Missile (Crateria)"]
loc.AccessFrom = {
    'Landing Site': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.canPassBombPassages(),
                       sm.traverse("ClimbRight"),
                       sm.haveItem('SpeedBooster'),
                       # reserves are hard to trigger midspark when not having ETanks
                       sm.wor(sm.wand(sm.energyReserveCountOk(2), sm.itemCountOk('ETank', 1)), # need energy to get out
                              sm.wand(sm.itemCountOk('ETank', 1),
                                      sm.wor(sm.haveItem('Grapple'), # use grapple/space or dmg protection to get out
                                             sm.haveItem('SpaceJump'),
                                             sm.heatProof()))),
                       sm.wor(sm.haveItem('Ice'),
                              sm.wand(sm.canSimpleShortCharge(), sm.canUsePowerBombs()))) # there's also a dboost involved in simple short charge or you have to kill the yellow enemies with some power bombs
)


loc = locationsDict["Missile (Crateria middle)"]
loc.AccessFrom = {
    'Landing Site': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.canPassBombPassages()
)


loc = locationsDict["Power Bomb (green Brinstar bottom)"]
loc.AccessFrom = {
    'Etecoons Bottom': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.haveItem('Morph'),
                       sm.canKillBeetoms())
)


loc = locationsDict["Super Missile (pink Brinstar)"]
loc.AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wor(sm.wand(sm.traverse('BigPinkTopRight'),
                              sm.haveItem('SporeSpawn')),
                      # back way into spore spawn
                      sm.wand(sm.knowsSporeSpawnBackDoor(),
                              sm.canOpenGreenDoors(),
                              sm.canPassBombPassages()))
)
loc.PostAvailable = (
    lambda sm: sm.wand(sm.canOpenGreenDoors(),
                       sm.canPassBombPassages())
)


loc = locationsDict["Missile (green Brinstar below super missile)"]
loc.AccessFrom = {
    'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
}
loc.Available = (
    lambda sm: SMBool(True)
)
loc.PostAvailable = (
    lambda sm: sm.wor(RomPatches.has(RomPatches.EarlySupersShotBlock), sm.canPassBombPassages())
)


loc = locationsDict["Super Missile (green Brinstar top)"]
loc.AccessFrom = {
    'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
}
loc.Available = (
    lambda sm: sm.wor(sm.canMockball(),
                      sm.haveItem('SpeedBooster'))
)


loc = locationsDict["Missile (green Brinstar behind missile)"]
loc.AccessFrom = {
    'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
}
loc.Available = (
    lambda sm: sm.wand(sm.haveItem('Morph'),
                       sm.wor(sm.canMockball(),
                              sm.haveItem('SpeedBooster')),
                       sm.traverse('EarlySupersRight'),
                       sm.wor(sm.canPassBombPassages(),
                              sm.wand(sm.knowsRonPopeilScrew(),
                                      sm.haveItem('ScrewAttack'))))
)


loc = locationsDict["Missile (green Brinstar behind reserve tank)"]
loc.AccessFrom = {
    'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
}
loc.Available = (
    lambda sm: sm.wand(sm.traverse('EarlySupersRight'),
                       sm.haveItem('Morph'),
                       sm.wor(sm.canMockball(),
                              sm.haveItem('SpeedBooster')))
)


loc = locationsDict["Missile (pink Brinstar top)"]
loc.AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Missile (pink Brinstar bottom)"]
loc.AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Power Bomb (pink Brinstar)"]
loc.AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.canUsePowerBombs(),
                       sm.haveItem('Super'))
)


loc = locationsDict["Missile (green Brinstar pipe)"]
loc.AccessFrom = {
    'Green Hill Zone Top Right': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.haveItem('Morph')
)


loc = locationsDict["Power Bomb (blue Brinstar)"]
loc.AccessFrom = {
    'Blue Brinstar Elevator Bottom': lambda sm: sm.canUsePowerBombs(),
    'Morph Ball Room Left': lambda sm: sm.wor(sm.canPassBombPassages(),
                                              sm.wand(sm.haveItem('Morph'),
                                                      sm.canShortCharge())) # speedball
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Missile (blue Brinstar middle)"]
loc.AccessFrom = {
    'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.wor(RomPatches.has(RomPatches.BlueBrinstarMissile), sm.haveItem('Morph')),
                       sm.wor(RomPatches.has(RomPatches.BlueBrinstarBlueDoor), sm.traverse('ConstructionZoneRight')))
)


loc = locationsDict["Super Missile (green Brinstar bottom)"]
loc.AccessFrom = {
    'Etecoons Supers': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Missile (blue Brinstar bottom)"]
loc.AccessFrom = {
    'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.haveItem('Morph')
)


loc = locationsDict["Missile (blue Brinstar top)"]
loc.AccessFrom = {
    'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.canAccessBillyMays()
)


loc = locationsDict["Missile (blue Brinstar behind missile)"]
loc.AccessFrom = {
    'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.canAccessBillyMays()
)


loc = locationsDict["Power Bomb (red Brinstar sidehopper room)"]
loc.AccessFrom = {
    'Red Brinstar Elevator': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.traverse('RedTowerElevatorTopLeft'),
                       sm.canUsePowerBombs())
)


loc = locationsDict["Power Bomb (red Brinstar spike room)"]
loc.AccessFrom = {
    'Red Brinstar Elevator': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.traverse('RedTowerElevatorBottomLeft')
)


loc = locationsDict["Missile (red Brinstar spike room)"]
loc.AccessFrom = {
    'Red Brinstar Elevator': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.traverse('RedTowerElevatorBottomLeft'),
                       sm.canUsePowerBombs())
)


loc = locationsDict["Missile (Kraid)"]
loc.AccessFrom = {
    'Warehouse Zeela Room Left': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.canUsePowerBombs()
)


loc = locationsDict["Missile (lava room)"]
loc.AccessFrom = {
    'Cathedral': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.haveItem('Morph')
)


loc = locationsDict["Missile (below Ice Beam)"]
loc.AccessFrom = {
    'Business Center': lambda sm: sm.wand(sm.traverse('BusinessCenterTopLeft'),
                                          sm.canUsePowerBombs(),
                                          sm.canHellRun(**Settings.hellRunsTable['Ice']['Norfair Entrance -> Ice Beam']),
                                          sm.wor(sm.wand(sm.haveItem('Morph'),
                                                         sm.knowsMockball()),
                                                 sm.haveItem('SpeedBooster'))),
    'Crocomire Speedway Bottom': lambda sm: sm.wand(sm.canUseCrocRoomToChargeSpeed(),
                                                    sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Croc -> Ice Missiles']),
                                                    sm.haveItem('SpeedBooster'),
                                                    sm.knowsIceMissileFromCroc())
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Missile (above Crocomire)"]
loc.AccessFrom = {
    'Grapple Escape': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Missile (Hi-Jump Boots)"]
loc.AccessFrom = {
    'Business Center': lambda sm: sm.wor(RomPatches.has(RomPatches.HiJumpAreaBlueDoor), sm.traverse('BusinessCenterBottomLeft'))
}
loc.Available = (
    lambda sm: sm.haveItem('Morph')
)
loc.PostAvailable = (
    lambda sm: sm.wor(sm.canPassBombPassages(),
                      sm.wand(RomPatches.has(RomPatches.HiJumpShotBlock), sm.haveItem('Morph')))
)


loc = locationsDict["Energy Tank (Hi-Jump Boots)"]
loc.AccessFrom = {
    'Business Center': lambda sm: sm.wor(RomPatches.has(RomPatches.HiJumpAreaBlueDoor), sm.traverse('BusinessCenterBottomLeft'))
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Power Bomb (Crocomire)"]
loc.AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.traverse('PostCrocomireUpperLeft'),
                       sm.haveItem('Crocomire'),
                       sm.wor(sm.wor(sm.canFly(),
                                     sm.haveItem('Grapple'),
                                     sm.wand(sm.haveItem('SpeedBooster'),
                                             sm.wor(sm.heatProof(),
                                                    sm.energyReserveCountOk(1)))), # spark from the room before
                              sm.wor(sm.haveItem('HiJump'), # run and jump from yellow platform
                                     sm.wand(sm.haveItem('Ice'),
                                             sm.knowsCrocPBsIce()),
                                     sm.knowsCrocPBsDBoost())))
)


loc = locationsDict["Missile (below Crocomire)"]
loc.AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.traverse('PostCrocomireShaftRight'), sm.haveItem('Crocomire'), sm.haveItem('Morph'))
)


loc = locationsDict["Missile (Grapple Beam)"]
loc.AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.haveItem('Crocomire'),
                       sm.wor(sm.wor(sm.wand(sm.haveItem('Morph'), # from below
                                             sm.canFly()),
                                     sm.wand(sm.haveItem('SpeedBooster'),
                                             sm.wor(sm.knowsShortCharge(),
                                                    sm.canUsePowerBombs()))),
                              sm.wand(sm.canGreenGateGlitch(), # from grapple room
                                      sm.canFly()))) # TODO::test if accessible with a spark (short charge), and how many etanks required
)
loc.PostAvailable = (
    lambda sm: sm.wor(sm.haveItem('Morph'), # normal exit
                      sm.wand(sm.haveItem('Super'), # go back to grapple room
                              sm.wor(sm.haveItem('SpaceJump'),
                                     sm.wand(sm.haveItem('SpeedBooster'), sm.haveItem('HiJump'))))) # jump from the yellow plateform ennemy
)


loc = locationsDict["Missile (Norfair Reserve Tank)"]
loc.AccessFrom = {
    'Bubble Mountain': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutain(),
    'Bubble Mountain Top': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutainTop()
}
loc.Available = (
    lambda sm: sm.wand(sm.haveItem('Morph'), sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Norfair Reserve']))
)


loc = locationsDict["Missile (bubble Norfair green door)"]
loc.AccessFrom = {
    'Bubble Mountain': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutain(),
    'Bubble Mountain Top': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutainTop()
}
loc.Available = (
    lambda sm: sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Norfair Reserve Missiles'])
)


loc = locationsDict["Missile (bubble Norfair)"]
loc.AccessFrom = {
    'Bubble Mountain': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Missile (Speed Booster)"]
loc.AccessFrom = {
    'Bubble Mountain Top': lambda sm: sm.wor(RomPatches.has(RomPatches.SpeedAreaBlueDoors),
                                             sm.traverse('BubbleMountainTopRight'))
}
loc.Available = (
    lambda sm: sm.canHellRunToSpeedBooster()
)
loc.PostAvailable = (
    lambda sm: sm.canHellRunBackFromSpeedBoosterMissile()
)


loc = locationsDict["Missile (Wave Beam)"]
loc.AccessFrom = {
    'Bubble Mountain Top': lambda sm: sm.canAccessDoubleChamberItems()
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Missile (Gold Torizo)"]
loc.AccessFrom = {
    'LN Above GT': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
)
loc.PostAvailable = (
    lambda sm: sm.enoughStuffGT()
)


loc = locationsDict["Super Missile (Gold Torizo)"]
loc.AccessFrom = {
    'Screw Attack Bottom': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.canDestroyBombWalls()
)
loc.PostAvailable = (
    lambda sm: sm.enoughStuffGT()
)


loc = locationsDict["Missile (Mickey Mouse room)"]
loc.AccessFrom = {
    'Worst Room Top': lambda sm: sm.canPassBombPassages()
}
loc.Available = (
    lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
)


loc = locationsDict["Missile (lower Norfair above fire flea room)"]
loc.AccessFrom = {
    'Firefleas': lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Power Bomb (lower Norfair above fire flea room)"]
loc.AccessFrom = {
    'Firefleas Top': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Power Bomb (Power Bombs of shame)"]
loc.AccessFrom = {
    'Wasteland': lambda sm: sm.canUsePowerBombs()
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Missile (lower Norfair near Wave Beam)"]
loc.AccessFrom = {
    'Firefleas': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                       sm.canDestroyBombWalls(),
                       sm.haveItem('Morph'))
)


loc = locationsDict["Missile (Wrecked Ship middle)"]
loc.AccessFrom = {
    'Wrecked Ship Main': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.canPassBombPassages()
)


loc = locationsDict["Missile (Gravity Suit)"]
loc.AccessFrom = {
    'Bowling': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Missile (Wrecked Ship top)"]
loc.AccessFrom = {
    'Wrecked Ship Main': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: Bosses.bossDead(sm, 'Phantoon')
)


loc = locationsDict["Super Missile (Wrecked Ship left)"]
loc.AccessFrom = {
    'Wrecked Ship Main': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: Bosses.bossDead(sm, 'Phantoon')
)


loc = locationsDict["Missile (green Maridia shinespark)"]
loc.AccessFrom = {
    'Main Street Bottom': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wand(sm.haveItem('Gravity'),
                       sm.haveItem('SpeedBooster'),
                       sm.wor(sm.wand(sm.traverse('MainStreetBottomRight'), # run from room on the right
                                      sm.wor(RomPatches.has(RomPatches.AreaRandoGatesOther),
                                             sm.haveItem('Super')),
                                      sm.itemCountOk('ETank', 1)), # etank for the spark since sparking from low ground
                              sm.canSimpleShortCharge())) # run from above
)


loc = locationsDict["Super Missile (green Maridia)"]
loc.AccessFrom = {
    'Main Street Bottom': lambda sm: sm.canDoOuterMaridia()
}
loc.Available = (
    lambda sm: sm.haveItem('Morph')
)


loc = locationsDict["Missile (green Maridia tatori)"]
loc.AccessFrom = {
    'Main Street Bottom': lambda sm: sm.wand(sm.wor(sm.traverse('FishTankRight'),
                                                    RomPatches.has(RomPatches.MamaTurtleBlueDoor)),
                                             sm.canDoOuterMaridia()),
    'Mama Turtle': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Super Missile (yellow Maridia)"]
loc.AccessFrom = {
    'Watering Hole Bottom': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Missile (yellow Maridia super missile)"]
loc.AccessFrom = {
    'Watering Hole Bottom': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Missile (yellow Maridia false wall)"]
loc.AccessFrom = {
    'Beach': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Missile (left Maridia sand pit room)"]
loc.AccessFrom = {
    'Left Sandpit': lambda sm: sm.canClimbWestSandHole()
}
loc.Available = (
    lambda sm: sm.canAccessItemsInWestSandHole()
)


loc = locationsDict["Missile (right Maridia sand pit room)"]
loc.AccessFrom = {
    'Right Sandpit': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: sm.wor(sm.haveItem('Gravity'),
                      sm.wand(sm.haveItem('HiJump'),
                              sm.knowsGravLessLevel3()))
)


loc = locationsDict["Power Bomb (right Maridia sand pit room)"]
loc.AccessFrom = {
    'Right Sandpit': lambda sm: sm.haveItem('Morph')
}
loc.Available = (
    lambda sm: sm.wor(sm.haveItem('Gravity'),
                      sm.wand(sm.knowsGravLessLevel3(),
                              sm.haveItem('HiJump'),
                              sm.canSpringBallJump())) # https://www.youtube.com/watch?v=7LYYxphRRT0
)


loc = locationsDict["Missile (pink Maridia)"]
loc.AccessFrom = {
    'Aqueduct': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Super Missile (pink Maridia)"]
loc.AccessFrom = {
    'Aqueduct': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)


loc = locationsDict["Missile (Draygon)"]
loc.AccessFrom = {
    'Precious Room Top': lambda sm: SMBool(True)
}
loc.Available = (
    lambda sm: SMBool(True)
)

# TODO::use the dict in solver/randomizer
# create the list that the solver/randomizer use
locations = [loc for loc in locationsDict.values()]

def postLoad():
    type(locationsDict["Reserve Tank, Wrecked Ship"]).Address = Addresses.getOne("bank_8f_Room_C98E_Reserve")
    type(locationsDict["Missile (Gravity Suit)"]).Address = Addresses.getOne("bank_8f_Room_C98E_Missile")

    type(locationsDict["Energy Tank, Gauntlet"]).MapAttrs = LocationMapAttrs(17, 3, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)
    type(locationsDict["Bomb"]).MapAttrs = LocationMapAttrs(25, 7, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)
    type(locationsDict["Energy Tank, Terminator"]).MapAttrs = LocationMapAttrs(12, 7, LocationMapTileKind.ThreeWallsOneDoorOpenRight, hFlip=False, vFlip=False)
    type(locationsDict["Reserve Tank, Brinstar"]).MapAttrs = LocationMapAttrs(13, 5, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)
    type(locationsDict["Charge Beam"]).MapAttrs = LocationMapAttrs(17, 12, LocationMapTileKind.ThreeWallsOpenBottom, hFlip=False, vFlip=True)
    type(locationsDict["Morphing Ball"]).MapAttrs = LocationMapAttrs(25, 11, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)
    type(locationsDict["Energy Tank, Brinstar Ceiling"]).MapAttrs = LocationMapAttrs(31, 11, LocationMapTileKind.TwoWallsCorridor, hFlip=False, vFlip=False)
    type(locationsDict["Energy Tank, Etecoons"]).MapAttrs = LocationMapAttrs(6, 11, LocationMapTileKind.ThreeWallsOneDoorOpenRight, hFlip=False, vFlip=False)
    type(locationsDict["Energy Tank, Waterway"]).MapAttrs = LocationMapAttrs(8, 14, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)
    type(locationsDict["Energy Tank, Brinstar Gate"]).MapAttrs = LocationMapAttrs(21, 9, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)
    type(locationsDict["X-Ray Scope"]).MapAttrs = LocationMapAttrs(23, 16, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)
    type(locationsDict["Spazer"]).MapAttrs = LocationMapAttrs(38, 18, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)
    type(locationsDict["Energy Tank, Kraid"]).MapAttrs = LocationMapAttrs(43, 20, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)
    type(locationsDict["Varia Suit"]).MapAttrs = LocationMapAttrs(57, 20, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)
    type(locationsDict["Ice Beam"]).MapAttrs = LocationMapAttrs(5, 3, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)
    type(locationsDict["Energy Tank, Crocomire"]).MapAttrs = LocationMapAttrs(19, 11, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Hi-Jump Boots"]).MapAttrs = LocationMapAttrs(7, 7, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)
    type(locationsDict["Grapple Beam"]).MapAttrs = LocationMapAttrs(3, 17, LocationMapTileKind.ThreeWallsOneDoorOpenBottom, hFlip=True, vFlip=True)
    type(locationsDict["Reserve Tank, Norfair"]).MapAttrs = LocationMapAttrs(18, 3, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)
    type(locationsDict["Speed Booster"]).MapAttrs = LocationMapAttrs(37, 3, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)
    type(locationsDict["Wave Beam"]).MapAttrs = LocationMapAttrs(29, 5, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)
    type(locationsDict["Energy Tank, Ridley"]).MapAttrs = LocationMapAttrs(22, 18, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)
    type(locationsDict["Screw Attack"]).MapAttrs = LocationMapAttrs(20, 17, LocationMapTileKind.ThreeWallsOneDoorOpenBottom, hFlip=False, vFlip=True)
    type(locationsDict["Energy Tank, Firefleas"]).MapAttrs = LocationMapAttrs(37, 12, LocationMapTileKind.TwoWallsCorner, hFlip=True, vFlip=True)
    type(locationsDict["Reserve Tank, Wrecked Ship"]).MapAttrs = LocationMapAttrs(15, 12, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Energy Tank, Wrecked Ship"]).MapAttrs = LocationMapAttrs(18, 14, LocationMapTileKind.TwoWallsCorner, hFlip=False, vFlip=False)
    type(locationsDict["Right Super, Wrecked Ship"]).MapAttrs = LocationMapAttrs(21, 18, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Gravity Suit"]).MapAttrs = LocationMapAttrs(10, 14, LocationMapTileKind.FourWallsCorridor, hFlip=False, vFlip=False)
    type(locationsDict["Energy Tank, Mama turtle"]).MapAttrs = LocationMapAttrs(18, 13, LocationMapTileKind.TwoWallsCorner, hFlip=False, vFlip=False)
    type(locationsDict["Plasma Beam"]).MapAttrs = LocationMapAttrs(28, 3, LocationMapTileKind.TwoWallsCorner, hFlip=True, vFlip=True)
    type(locationsDict["Reserve Tank, Maridia"]).MapAttrs = LocationMapAttrs(20, 15, LocationMapTileKind.TwoWallsCorner, hFlip=False, vFlip=False)
    type(locationsDict["Spring Ball"]).MapAttrs = LocationMapAttrs(33, 17, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Energy Tank, Botwoon"]).MapAttrs = LocationMapAttrs(29, 9, LocationMapTileKind.TwoWallsCorridor, hFlip=False, vFlip=False)
    type(locationsDict["Space Jump"]).MapAttrs = LocationMapAttrs(38, 11, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)
    type(locationsDict["Power Bomb (Crateria surface)"]).MapAttrs = LocationMapAttrs(33, 2, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Missile (outside Wrecked Ship bottom)"]).MapAttrs = LocationMapAttrs(38, 6, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)
    type(locationsDict["Missile (outside Wrecked Ship top)"]).MapAttrs = LocationMapAttrs(39, 1, LocationMapTileKind.SingleWallHorizontal, hFlip=False, vFlip=False)
    type(locationsDict["Missile (outside Wrecked Ship middle)"]).MapAttrs = LocationMapAttrs(38, 3, LocationMapTileKind.SingleWallVertical, hFlip=False, vFlip=False)
    type(locationsDict["Missile (Crateria moat)"]).MapAttrs = LocationMapAttrs(36, 5, LocationMapTileKind.TwoWallsCornerWithHorizontalDoor, hFlip=False, vFlip=False)
    type(locationsDict["Missile (Crateria bottom)"]).MapAttrs = LocationMapAttrs(20, 19, LocationMapTileKind.ThreeWallsOpenBottom, hFlip=False, vFlip=True)
    type(locationsDict["Missile (Crateria gauntlet right)"]).MapAttrs = LocationMapAttrs(11, 4, LocationMapTileKind.ThreeWallsOpenBottom, hFlip=False, vFlip=True)
    type(locationsDict["Missile (Crateria gauntlet left)"]).MapAttrs = LocationMapAttrs(11, 4, LocationMapTileKind.ThreeWallsOpenBottom, hFlip=False, vFlip=True)
    type(locationsDict["Super Missile (Crateria)"]).MapAttrs = LocationMapAttrs(24, 10, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Missile (Crateria middle)"]).MapAttrs = LocationMapAttrs(16, 8, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)
    type(locationsDict["Power Bomb (green Brinstar bottom)"]).MapAttrs = LocationMapAttrs(12, 8, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Super Missile (pink Brinstar)"]).MapAttrs = LocationMapAttrs(24, 10, LocationMapTileKind.TwoWallsCornerWithPixel, hFlip=True, vFlip=True)
    type(locationsDict["Missile (green Brinstar below super missile)"]).MapAttrs = LocationMapAttrs(11, 5, LocationMapTileKind.TwoWallsCorridor, hFlip=False, vFlip=False)
    type(locationsDict["Super Missile (green Brinstar top)"]).MapAttrs = LocationMapAttrs(10, 4, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)
    type(locationsDict["Missile (green Brinstar behind missile)"]).MapAttrs = LocationMapAttrs(14, 5, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Missile (green Brinstar behind reserve tank)"]).MapAttrs = LocationMapAttrs(14, 5, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Missile (pink Brinstar top)"]).MapAttrs = LocationMapAttrs(17, 8, LocationMapTileKind.SingleWallVertical, hFlip=False, vFlip=False)
    type(locationsDict["Missile (pink Brinstar bottom)"]).MapAttrs = LocationMapAttrs(17, 11, LocationMapTileKind.TwoWallsCorner, hFlip=False, vFlip=True)
    type(locationsDict["Power Bomb (pink Brinstar)"]).MapAttrs = LocationMapAttrs(15, 9, LocationMapTileKind.TwoWallsCornerWithPixel, hFlip=False, vFlip=True)
    type(locationsDict["Missile (green Brinstar pipe)"]).MapAttrs = LocationMapAttrs(22, 12, LocationMapTileKind.TwoWallsCorner, hFlip=True, vFlip=False)
    type(locationsDict["Power Bomb (blue Brinstar)"]).MapAttrs = LocationMapAttrs(23, 11, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Missile (blue Brinstar middle)"]).MapAttrs = LocationMapAttrs(32, 11, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Super Missile (green Brinstar bottom)"]).MapAttrs = LocationMapAttrs(5, 11, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)
    type(locationsDict["Missile (blue Brinstar bottom)"]).MapAttrs = LocationMapAttrs(28, 12, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)
    type(locationsDict["Missile (blue Brinstar top)"]).MapAttrs = LocationMapAttrs(29, 9, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)
    type(locationsDict["Missile (blue Brinstar behind missile)"]).MapAttrs = LocationMapAttrs(29, 9, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)
    type(locationsDict["Power Bomb (red Brinstar sidehopper room)"]).MapAttrs = LocationMapAttrs(35, 9, LocationMapTileKind.ThreeWallsOpenBottom, hFlip=False, vFlip=True)
    type(locationsDict["Power Bomb (red Brinstar spike room)"]).MapAttrs = LocationMapAttrs(35, 12, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)
    type(locationsDict["Missile (red Brinstar spike room)"]).MapAttrs = LocationMapAttrs(34, 12, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)
    type(locationsDict["Missile (Kraid)"]).MapAttrs = LocationMapAttrs(47, 19, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Missile (lava room)"]).MapAttrs = LocationMapAttrs(16, 5, LocationMapTileKind.TwoWallsCornerWithHorizontalDoor, hFlip=True, vFlip=True)
    type(locationsDict["Missile (below Ice Beam)"]).MapAttrs = LocationMapAttrs(2, 5, LocationMapTileKind.ThreeWallsOneDoorOpenBottom, hFlip=True, vFlip=False)
    type(locationsDict["Missile (above Crocomire)"]).MapAttrs = LocationMapAttrs(11, 7, LocationMapTileKind.TwoWallsCornerWithHorizontalDoor, hFlip=False, vFlip=False)
    type(locationsDict["Missile (Hi-Jump Boots)"]).MapAttrs = LocationMapAttrs(8, 6, LocationMapTileKind.TwoWallsCornerWithPixel, hFlip=False, vFlip=False)
    type(locationsDict["Energy Tank (Hi-Jump Boots)"]).MapAttrs = LocationMapAttrs(9, 6, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)
    type(locationsDict["Power Bomb (Crocomire)"]).MapAttrs = LocationMapAttrs(9, 11, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)
    type(locationsDict["Missile (below Crocomire)"]).MapAttrs = LocationMapAttrs(14, 16, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Missile (Grapple Beam)"]).MapAttrs = LocationMapAttrs(8, 16, LocationMapTileKind.TwoWallsCorner, hFlip=True, vFlip=False)
    type(locationsDict["Missile (Norfair Reserve Tank)"]).MapAttrs = LocationMapAttrs(18, 3, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)
    type(locationsDict["Missile (bubble Norfair green door)"]).MapAttrs = LocationMapAttrs(21, 3, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)
    type(locationsDict["Missile (bubble Norfair)"]).MapAttrs = LocationMapAttrs(23, 6, LocationMapTileKind.TwoWallsCorner, hFlip=True, vFlip=True)
    type(locationsDict["Missile (Speed Booster)"]).MapAttrs = LocationMapAttrs(36, 3, LocationMapTileKind.ThreeWallsOneDoorOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Missile (Wave Beam)"]).MapAttrs = LocationMapAttrs(26, 5, LocationMapTileKind.SingleWallHorizontal, hFlip=False, vFlip=False)
    type(locationsDict["Missile (Gold Torizo)"]).MapAttrs = LocationMapAttrs(18, 16, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)
    type(locationsDict["Super Missile (Gold Torizo)"]).MapAttrs = LocationMapAttrs(19, 16, LocationMapTileKind.TwoWallsCorner, hFlip=True, vFlip=False)
    type(locationsDict["Missile (Mickey Mouse room)"]).MapAttrs = LocationMapAttrs(28, 11, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)
    type(locationsDict["Missile (lower Norfair above fire flea room)"]).MapAttrs = LocationMapAttrs(35, 6, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Power Bomb (lower Norfair above fire flea room)"]).MapAttrs = LocationMapAttrs(37, 7, LocationMapTileKind.FourWallsTwoDoors, hFlip=True, vFlip=True)
    type(locationsDict["Power Bomb (Power Bombs of shame)"]).MapAttrs = LocationMapAttrs(32, 15, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)
    type(locationsDict["Missile (lower Norfair near Wave Beam)"]).MapAttrs = LocationMapAttrs(29, 6, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)
    type(locationsDict["Missile (Wrecked Ship middle)"]).MapAttrs = LocationMapAttrs(12, 17, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)
    type(locationsDict["Missile (Gravity Suit)"]).MapAttrs = LocationMapAttrs(13, 14, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Missile (Wrecked Ship top)"]).MapAttrs = LocationMapAttrs(21, 11, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)
    type(locationsDict["Super Missile (Wrecked Ship left)"]).MapAttrs = LocationMapAttrs(15, 18, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)
    type(locationsDict["Missile (green Maridia shinespark)"]).MapAttrs = LocationMapAttrs(10, 13, LocationMapTileKind.SingleWallVertical, hFlip=False, vFlip=False)
    type(locationsDict["Super Missile (green Maridia)"]).MapAttrs = LocationMapAttrs(11, 12, LocationMapTileKind.SingleWallVertical, hFlip=True, vFlip=False)
    type(locationsDict["Missile (green Maridia tatori)"]).MapAttrs = LocationMapAttrs(19, 14, LocationMapTileKind.SingleWallVertical, hFlip=True, vFlip=False)
    type(locationsDict["Super Missile (yellow Maridia)"]).MapAttrs = LocationMapAttrs(12, 7, LocationMapTileKind.ThreeWallsOpenBottom, hFlip=False, vFlip=True)
    type(locationsDict["Missile (yellow Maridia super missile)"]).MapAttrs = LocationMapAttrs(12, 7, LocationMapTileKind.ThreeWallsOpenBottom, hFlip=False, vFlip=True)
    type(locationsDict["Missile (yellow Maridia false wall)"]).MapAttrs = LocationMapAttrs(20, 7, LocationMapTileKind.TwoWallsCorner, hFlip=True, vFlip=True)
    type(locationsDict["Missile (left Maridia sand pit room)"]).MapAttrs = LocationMapAttrs(20, 15, LocationMapTileKind.TwoWallsCorner, hFlip=False, vFlip=False)
    type(locationsDict["Missile (right Maridia sand pit room)"]).MapAttrs = LocationMapAttrs(23, 15, LocationMapTileKind.TwoWallsCorner, hFlip=False, vFlip=False)
    type(locationsDict["Power Bomb (right Maridia sand pit room)"]).MapAttrs = LocationMapAttrs(24, 16, LocationMapTileKind.TwoWallsCornerWithVerticalDoor, hFlip=True, vFlip=True)
    type(locationsDict["Missile (pink Maridia)"]).MapAttrs = LocationMapAttrs(24, 10, LocationMapTileKind.SingleWallHorizontal, hFlip=False, vFlip=False)
    type(locationsDict["Super Missile (pink Maridia)"]).MapAttrs = LocationMapAttrs(25, 10, LocationMapTileKind.TwoWallsCorner, hFlip=True, vFlip=False)
    type(locationsDict["Missile (Draygon)"]).MapAttrs = LocationMapAttrs(42, 8, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)


class LocationsHelper:
    # used by FillerRandom to know how many front fill steps it must perform
    def getRandomFillHelp(startLocation):
        helpByAp = {
            "Firefleas Top": 3,
            "Aqueduct": 1,
            "Mama Turtle": 1,
            "Watering Hole": 2,
            "Etecoons Supers": 2,
            "Gauntlet Top":1,
            "Bubble Mountain":1
        }
        return helpByAp[startLocation] if startLocation in helpByAp else 0

    # for a given start AP, gives:
    # - locations that can be used as majors/chozo in the start area
    # - locations to preserve in the split
    # - number of necessary majors locations to add in the start area,
    # - number of necessary chozo locations to add in the start area
    # locs are taken in the first n in the list
    def getStartMajors(startLocation):
        majLocsByAp = {
            'Gauntlet Top': ([
                "Missile (Crateria gauntlet right)",
                "Missile (Crateria gauntlet left)"
            ], ["Energy Tank, Terminator"], 1, 2),
            'Green Brinstar Elevator': ([
                "Missile (green Brinstar below super missile)"
            ], ["Reserve Tank, Brinstar"], 1, 1),
            'Big Pink': ([
                "Missile (pink Brinstar top)",
                "Missile (pink Brinstar bottom)"
            ], ["Charge Beam"], 1, 2),
            'Etecoons Supers': ([
                "Energy Tank, Etecoons",
                "Super Missile (green Brinstar bottom)",
            ], ["Energy Tank, Etecoons"], 1, 2),
            'Firefleas Top': ([
                "Power Bomb (lower Norfair above fire flea room)",
                "Energy Tank, Firefleas",
                "Missile (lower Norfair near Wave Beam)",
                "Missile (lower Norfair above fire flea room)"
            ], ["Energy Tank, Firefleas"], 3, 4),
            'Business Center': ([
                "Energy Tank (Hi-Jump Boots)",
            ], ["Hi-Jump Boots"], 1, 1),
            'Bubble Mountain': ([
                "Missile (bubble Norfair)"
            ], ["Speed Booster", "Wave Beam"], 1, 1),
            'Mama Turtle': ([
                "Energy Tank, Mama turtle",
                "Missile (green Maridia tatori)",
                "Super Missile (green Maridia)"
            ], ["Energy Tank, Mama turtle"], 2, 3),
            'Watering Hole': ([
                "Missile (yellow Maridia super missile)",
                "Super Missile (yellow Maridia)",
                "Missile (yellow Maridia false wall)"
            ], [], 2, 3),
            'Aqueduct': ([
                "Missile (pink Maridia)",
                "Super Missile (pink Maridia)",
                "Missile (right Maridia sand pit room)"
            ], ["Reserve Tank, Maridia"], 2, 3)
        }
        return majLocsByAp[startLocation] if startLocation in majLocsByAp else ([],[],0,0)
