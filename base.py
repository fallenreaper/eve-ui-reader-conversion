# module EveOnline.ParseUserinterface exposing (..)
# -| A library of building blocks to build programs that read from the EVE Online game client.
# The EVE Online client's UI tree can contain thousands of nodes and tens of thousands of individual properties. Because of this large amount of datanavigating in there can be time-consuming.
# This library helps us navigate the UI tree with functions to filter out redundant data and extract the interesting bits.
# The types in this module provide names more closely related to players' experiencesuch as the overview window or ship modules.
# To learn about the user interface structures in the EVE Online game clientsee the guide at <https://to.botlab.org/guide/parsed-user-interface-of-the-eve-online-game-client>
# -
# import Common.EffectOnWindow
# import Dict
# import EveOnline.MemoryReading
# import Json.Decode
# import List.Extra
# import Maybe.Extra
# import Regex
# import Set

from classes import *
from typing import Callable
from helpers import *
from copy import copy

from pprint import pprint


def parseUITreeWithDisplayRegionFromUITree(uiTree: UITreeNode) -> UITreeNodeWithDisplayRegion:
    selfDisplayRegion = getDisplayRegionFromDictEntries(
        uiTree) or DisplayRegion(**{'x': 0, 'y': 0, 'width': 0, 'height': 0})
    return asUITreeNodeWithDisplayRegion(selfDisplayRegion, selfDisplayRegion, uiTree)
# parseUITreeWithDisplayRegionFromUITree : UITreeNode -> UITreeNodeWithDisplayRegion
# parseUITreeWithDisplayRegionFromUITree uiTree =
#     let
#         selfDisplayRegion =
#             uiTree |> getDisplayRegionFromDictEntries |> Maybe.withDefault { x = 0, y = 0, width = 0, height = 0 }
#     in
#     uiTree
#         |> asUITreeNodeWithDisplayRegion
#             { selfDisplayRegion = selfDisplayRegion
#             , totalDisplayRegion = selfDisplayRegion
#             }


def parseUserinterfaceFromUITree(uiTree: UITreeNodeWithDisplayRegion) -> ParsedUserInterface:
    x = ParsedUserInterface()
    x.uiTree = uiTree
    x.contextMenus = parseContextMenusFromUITreeRoot(uiTree)
    x.shipUI = parseShipUIFromUITreeRoot(uiTree)
    x.targets = parseTargetsFromUITreeRoot(uiTree)
    x.infoPanelContainer = parseInfoPanelContainerFromUIRoot(uiTree)
    x.overviewWindow = parseOverviewWindowFromUITreeRoot(uiTree)
    x.selectedItemWindow = parseSelectedItemWindowFromUITreeRoot(uiTree)
    x.dronesWindow = parseDronesWindowFromUITreeRoot(uiTree)
    x.fittingWindow = parseFittingWindowFromUITreeRoot(uiTree)
    x.probeScannerWindow = parseProbeScannerWindowFromUITreeRoot(uiTree)
    x.directionalScannerWindow = parseDirectionalScannerWindowFromUITreeRoot(
        uiTree)
    x.stationWindow = parseStationWindowFromUITreeRoot(uiTree)
    x.inventoryWindows = parseInventoryWindowsFromUITreeRoot(uiTree)
    x.moduleButtonTooltip = parseModuleButtonTooltipFromUITreeRoot(uiTree)
    x.chatWindowStacks = parseChatWindowStacksFromUITreeRoot(uiTree)
    x.agentConversationWindows = parseAgentConversationWindowsFromUITreeRoot(
        uiTree)
    x.marketOrdersWindow = parseMarketOrdersWindowFromUITreeRoot(uiTree)
    x.surveyScanWindow = parseSurveyScanWindowFromUITreeRoot(uiTree)
    x.bookmarkLocationWindow = parseBookmarkLocationWindowFromUITreeRoot(
        uiTree)
    x.repairShopWindow = parseRepairShopWindowFromUITreeRoot(uiTree)
    x.characterSheetWindow = parseCharacterSheetWindowFromUITreeRoot(uiTree)
    x.fleetWindow = parseFleetWindowFromUITreeRoot(uiTree)
    x.watchListPanel = parseWatchListPanelFromUITreeRoot(uiTree)
    x.standaloneBookmarkWindow = parseStandaloneBookmarkWindowFromUITreeRoot(
        uiTree)
    x.neocom = parseNeocomFromUITreeRoot(uiTree)
    x.messageBoxes = parseMessageBoxesFromUITreeRoot(uiTree)
    x.layerAbovemain = parseLayerAbovemainFromUITreeRoot(uiTree)
    x.keyActivationWindow = parseKeyActivationWindowFromUITreeRoot(uiTree)
    return x


# parseUserinterfaceFromUITree : UITreeNodeWithDisplayRegion -> ParsedUserinterface
# parseUserinterfaceFromUITree uiTree =
#     { uiTree = uiTree
#     , contextMenus = parseContextMenusFromUITreeRoot uiTree
#     , shipUI = parseShipUIFromUITreeRoot uiTree
#     , targets = parseTargetsFromUITreeRoot uiTree
#     , infoPanelContainer = parseInfoPanelContainerFromUIRoot uiTree
#     , overviewWindow = parseOverviewWindowFromUITreeRoot uiTree
#     , selectedItemWindow = parseSelectedItemWindowFromUITreeRoot uiTree
#     , dronesWindow = parseDronesWindowFromUITreeRoot uiTree
#     , fittingWindow = parseFittingWindowFromUITreeRoot uiTree
#     , probeScannerWindow = parseProbeScannerWindowFromUITreeRoot uiTree
#     , directionalScannerWindow = parseDirectionalScannerWindowFromUITreeRoot uiTree
#     , stationWindow = parseStationWindowFromUITreeRoot uiTree
#     , inventoryWindows = parseInventoryWindowsFromUITreeRoot uiTree
#     , moduleButtonTooltip = parseModuleButtonTooltipFromUITreeRoot uiTree
#     , chatWindowStacks = parseChatWindowStacksFromUITreeRoot uiTree
#     , agentConversationWindows = parseAgentConversationWindowsFromUITreeRoot uiTree
#     , marketOrdersWindow = parseMarketOrdersWindowFromUITreeRoot uiTree
#     , surveyScanWindow = parseSurveyScanWindowFromUITreeRoot uiTree
#     , bookmarkLocationWindow = parseBookmarkLocationWindowFromUITreeRoot uiTree
#     , repairShopWindow = parseRepairShopWindowFromUITreeRoot uiTree
#     , characterSheetWindow = parseCharacterSheetWindowFromUITreeRoot uiTree
#     , fleetWindow = parseFleetWindowFromUITreeRoot uiTree
#     , watchListPanel = parseWatchListPanelFromUITreeRoot uiTree
#     , standaloneBookmarkWindow = parseStandaloneBookmarkWindowFromUITreeRoot uiTree
#     , neocom = parseNeocomFromUITreeRoot uiTree
#     , messageBoxes = parseMessageBoxesFromUITreeRoot uiTree
#     , layerAbovemain = parseLayerAbovemainFromUITreeRoot uiTree
#     , keyActivationWindow = parseKeyActivationWindowFromUITreeRoot uiTree
#     }

def unwrapUITreeNodeChild(child: UITreeNodeChild) -> UITreeNode:
    # print("Type of Child :", type(child))
    if type(child) == UITreeNodeChild: return child
    # if child is UITreeNodeChild:
    #     return child.

# unwrapUITreeNodeChild : UITreeNodeChild -> UITreeNode
# unwrapUITreeNodeChild child =
#     case child of
#         UITreeNodeChild node ->
#             node


def asUITreeNodeWithDisplayRegion(selfDisplayRegion: DisplayRegion, totalDisplayRegion: DisplayRegion, uiNode: UITreeNode) -> UITreeNodeWithDisplayRegion:
    x = UITreeNodeWithDisplayRegion()
    x.uiNode = uiNode
    dr = Location2d()
    dr.x = totalDisplayRegion.x
    dr.y = totalDisplayRegion.y
    x.children = [asUITreeNodeWithInheritedOffset(dr, unwrapUITreeNodeChild(x)) for x in uiNode.children if x is not None] if uiNode.children is not None else None  # TODO: for all children do `unwrapUITreeNodeChild`
    x.selfDisplayRegion = selfDisplayRegion
    x.totalDisplayRegion = totalDisplayRegion
    return x

# asUITreeNodeWithDisplayRegion : { selfDisplayRegion : DisplayRegion, totalDisplayRegion : DisplayRegion } -> UITreeNode -> UITreeNodeWithDisplayRegion
# asUITreeNodeWithDisplayRegion { selfDisplayRegion, totalDisplayRegion } uiNode =
#     { uiNode = uiNode
#     , children = uiNode.children |> Maybe.map (List.map (unwrapUITreeNodeChild >> asUITreeNodeWithInheritedOffset { x = totalDisplayRegion.x, y = totalDisplayRegion.y }))
#     , selfDisplayRegion = selfDisplayRegion
#     , totalDisplayRegion = totalDisplayRegion
#     }


def asUITreeNodeWithInheritedOffset(inheritedOffset:Location2d, rawNode: UITreeNode) -> UITreeNodeWithDisplayRegion:
    selfRegion = getDisplayRegionFromDictEntries(rawNode)
    if selfRegion is None:
        return ChildWithoutRegion(rawNode)
    a = copy(selfRegion)
    a.x += (inheritedOffset.x or 0)
    a.y += (inheritedOffset.y or 0)
    return asUITreeNodeWithDisplayRegion(selfRegion, a, rawNode)


# asUITreeNodeWithInheritedOffset : { x : int, y : int } -> UITreeNode -> ChildOfNodeWithDisplayRegion
# asUITreeNodeWithInheritedOffset inheritedOffset rawNode =
#     case rawNode |> getDisplayRegionFromDictEntries of
#         Nothing ->
#             ChildWithoutRegion rawNode
#         Just selfRegion ->
#             ChildWithRegion
#                 (asUITreeNodeWithDisplayRegion
#                     { selfDisplayRegion = selfRegion
#                     , totalDisplayRegion =
#                         { selfRegion | x = inheritedOffset.x + selfRegion.x, y = inheritedOffset.y + selfRegion.y }
#                     }
#                     rawNode
#                 )


def getDisplayRegionFromDictEntries(uiNode: UITreeNode) -> Optional[DisplayRegion]:
    def fixedNumberFromJsonValue(val: Union[int, str]):
        if type(val) is int:
            return val
        else:
            try:
                print("Val", val)
                if val is None: return 0
                if type(val) is dict:
                    return int(val.get("int_low32"))
                return int(val)
            except Exception as e:
                print("Excemption Parsing: ", e)
                return None

    def fixedNumberFromPropertyName(name: str) -> int:
        return fixedNumberFromJsonValue(uiNode.dictEntriesOfInterest.get(name))

    dr = DisplayRegion()
    dr.x = fixedNumberFromPropertyName("_displayX")
    dr.y = fixedNumberFromPropertyName("displayY")
    dr.width = fixedNumberFromPropertyName("_displayWidth")
    dr.height = fixedNumberFromPropertyName("_displayHeight")
    print("Display Region: ", vars(dr))
    return dr

# getDisplayRegionFromDictEntries : UITreeNode -> Maybe DisplayRegion
# getDisplayRegionFromDictEntries uiNode =
#     let
#         fixedNumberFromJsonValue =
#             Json.Decode.decodeValue
#                 (Json.Decode.oneOf
#                     [ jsonDecodeintFromintOrstr
#                     , Json.Decode.field "int_low32" jsonDecodeintFromintOrstr
#                     ]
#                 )
#         fixedNumberFromPropertyName propertyName =
#             uiNode.dictEntriesOfinterest
#                 |> Dict.get propertyName
#                 |> Maybe.andThen (fixedNumberFromJsonValue >> Result.toMaybe)
#     in
#     case
#         ( ( fixedNumberFromPropertyName "_displayX", fixedNumberFromPropertyName "_displayY" )
#         , ( fixedNumberFromPropertyName "_displayWidth", fixedNumberFromPropertyName "_displayHeight" )
#         )
#     of
#         ( ( Just displayX, Just displayY ), ( Just displayWidth, Just displayHeight ) ) ->
#             Just { x = displayX, y = displayY, width = displayWidth, height = displayHeight }
#         _ ->
#             Nothing


def parseContextMenusFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> List[ContextMenu]:
    pass

# parseContextMenusFromUITreeRoot : UITreeNodeWithDisplayRegion -> List ContextMenu
# parseContextMenusFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listChildrenWithDisplayRegion
#             |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map str.toLower >> (==) (Just "l_menu"))
#             |> List.head
#     of
#         Nothing ->
#             []
#         Just layerMenu ->
#             layerMenu
#                 |> listChildrenWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> str.toLower >> str.contains "menu")
#                 |> List.map parseContextMenu


def parseInfoPanelContainerFromUIRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[InfoPanelContainer]:
    pass
# parseContextMenusFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe InfoPanelContainer
# parseInfoPanelContainerFromUIRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "InfoPanelContainer")
#             |> List.sortBy (.uiNode >> countDescendantsInUITreeNode >> negate)
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just containerNode ->
#             Just
#                 { uiNode = containerNode
#                 , icons = parseInfoPanelIconsFromInfoPanelContainer containerNode
#                 , infoPanelLocationInfo = parseInfoPanelLocationInfoFromInfoPanelContainer containerNode
#                 , infoPanelRoute = parseInfoPanelRouteFromInfoPanelContainer containerNode
#                 , infoPanelAgentMissions = parseInfoPanelAgentMissionsFromInfoPanelContainer containerNode
#                 }


def parseInfoPanelIconsFromInfoPanelContainer(infoPanelContainerNode: UITreeNodeWithDisplayRegion) -> Optional[InfoPanelIcons]:
    pass

# parseInfoPanelIconsFromInfoPanelContainer : UITreeNodeWithDisplayRegion -> Maybe InfoPanelIcons
# parseInfoPanelIconsFromInfoPanelContainer infoPanelContainerNode =
#     case
#         infoPanelContainerNode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map ((==) "iconCont") >> Maybe.withDefault False)
#             |> List.sortBy (.totalDisplayRegion >> .y)
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just iconContainerNode ->
#             let
#                 iconNodeFromTexturePathEnd texturePathEnd =
#                     iconContainerNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter
#                             (.uiNode
#                                 >> getTexturePathFromDictEntries
#                                 >> Maybe.map (str.endsWith texturePathEnd)
#                                 >> Maybe.withDefault False
#                             )
#                         |> List.head
#             in
#             Just
#                 { uiNode = iconContainerNode
#                 , search = iconNodeFromTexturePathEnd "search.png"
#                 , locationInfo = iconNodeFromTexturePathEnd "LocationInfo.png"
#                 , route = iconNodeFromTexturePathEnd "Route.png"
#                 , agentMissions = iconNodeFromTexturePathEnd "Missions.png"
#                 , dailyChallenge = iconNodeFromTexturePathEnd "dailyChallenge.png"
#                 }


def parseInfoPanelLocationInfoFromInfoPanelContainer(infoPanelContainerNode: UITreeNodeWithDisplayRegion) -> Optional[InfoPanelLocationInfo]:
    pass
# parseInfoPanelLocationInfoFromInfoPanelContainer : UITreeNodeWithDisplayRegion -> Maybe InfoPanelLocationInfo
# parseInfoPanelLocationInfoFromInfoPanelContainer infoPanelContainerNode =
#     case
#         infoPanelContainerNode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "InfoPanelLocationInfo")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just infoPanelNode ->
#             let
#                 securityStatusPercent =
#                     infoPanelNode.uiNode
#                         |> getAllContainedDisplayTexts
#                         |> List.filterMap parseSecurityStatusPercentFromUINodeText
#                         |> List.head
#                 currentSolarSystemName =
#                     infoPanelNode.uiNode
#                         |> getAllContainedDisplayTexts
#                         |> List.filterMap parseCurrentSolarSystemFromUINodeText
#                         |> List.head
#                         |> Maybe.map str.trim
#                 maybeListSurroundingsButton =
#                     infoPanelNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ListSurroundingsBtn")
#                         |> List.head
#                 expandedContent =
#                     infoPanelNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter
#                             (\uiNode ->
#                                 (uiNode.uiNode.pythonObjectTypeName |> str.contains "Container")
#                                     && (uiNode.uiNode |> getNameFromDictEntries |> Maybe.withDefault "" |> str.contains "mainCont")
#                             )
#                         |> List.head
#                         |> Maybe.map
#                             (\expandedContainer ->
#                                 { currentStationName =
#                                     expandedContainer.uiNode
#                                         |> getAllContainedDisplayTexts
#                                         |> List.filterMap parseCurrentStationNameFromInfoPanelLocationInfoLabelText
#                                         |> List.head
#                                 }
#                             )
#             in
#             maybeListSurroundingsButton
#                 |> Maybe.map
#                     (\listSurroundingsButton ->
#                         { uiNode = infoPanelNode
#                         , listSurroundingsButton = listSurroundingsButton
#                         , currentSolarSystemName = currentSolarSystemName
#                         , securityStatusPercent = securityStatusPercent
#                         , expandedContent = expandedContent
#                         }
#                     )


def parseSecurityStatusPercentFromUINodeText(s: str) -> Optional[int]:
    pass
# parseSecurityStatusPercentFromUINodeText : str -> Maybe int
# parseSecurityStatusPercentFromUINodeText =
#     Maybe.Extra.oneOf
#         [ getSubstrBetweenXmlTagsAfterMarker "hint='Security status'"
#         , getSubstrBetweenXmlTagsAfterMarker "hint=\"Security status\"><color="
#         ]
#         >> Maybe.andThen (str.trim >> str.toFloat)
#         >> Maybe.map ((*) 100 >> round)


def parseCurrentSolarSystemFromUINodeText(s: str) -> Optional[str]:
    pass
# parseCurrentSolarSystemFromUINodeText : str -> Maybe str
# parseCurrentSolarSystemFromUINodeText =
#     Maybe.Extra.oneOf
#         [ getSubstrBetweenXmlTagsAfterMarker "alt='Current Solar System'"
#         , getSubstrBetweenXmlTagsAfterMarker "alt=\"Current Solar System\""
#         ]


def parseCurrentStationNameFromInfoPanelLocationInfoLabelText(s: str) -> Optional[str]:
    pass
# parseCurrentStationNameFromInfoPanelLocationInfoLabelText : str -> Maybe str
# parseCurrentStationNameFromInfoPanelLocationInfoLabelText =
#     getSubstrBetweenXmlTagsAfterMarker "alt='Current Station'"
#         >> Maybe.map str.trim


def parseInfoPanelRouteFromInfoPanelContainer(infoPanelContainerNode: UITreeNodeWithDisplayRegion) -> Optional[InfoPanelRoute]:
    pass
# parseInfoPanelRouteFromInfoPanelContainer : UITreeNodeWithDisplayRegion -> Maybe InfoPanelRoute
# parseInfoPanelRouteFromInfoPanelContainer infoPanelContainerNode =
#     case
#         infoPanelContainerNode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "InfoPanelRoute")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just infoPanelRouteNode ->
#             let
#                 routeElementMarker =
#                     infoPanelRouteNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "AutopilotDestinationIcon")
#                         |> List.map (\uiNode -> { uiNode = uiNode })
#             in
#             Just { uiNode = infoPanelRouteNode, routeElementMarker = routeElementMarker }


def parseInfoPanelAgentMissionsFromInfoPanelContainer(infoPanelContainerNode: UITreeNodeWithDisplayRegion) -> Optional[InfoPanelAgentMissions]:
    pass
# parseInfoPanelAgentMissionsFromInfoPanelContainer : UITreeNodeWithDisplayRegion -> Maybe InfoPanelAgentMissions
# parseInfoPanelAgentMissionsFromInfoPanelContainer infoPanelContainerNode =
#     case
#         infoPanelContainerNode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "InfoPanelAgentMissions")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just infoPanelNode ->
#             let
#                 entries =
#                     infoPanelNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "MissionEntry")
#                         |> List.map (\uiNode -> { uiNode = uiNode })
#             in
#             Just
#                 { uiNode = infoPanelNode
#                 , entries = entries
#                 }


def parseContextMenu(contextMenuUINOde: UITreeNodeWithDisplayRegion) -> ContextMenu:
    pass
# parseContextMenu : UITreeNodeWithDisplayRegion -> ContextMenu
# parseContextMenu contextMenuUINode =
#     let
#         entriesUINodes =
#             contextMenuUINode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> str.toLower >> str.contains "menuentry")
#         entries =
#             entriesUINodes
#                 |> List.map
#                     (\entryUINode ->
#                         let
#                             text =
#                                 entryUINode
#                                     |> listDescendantsWithDisplayRegion
#                                     |> List.filterMap (.uiNode >> getDisplayText)
#                                     |> List.sortBy (str.length >> negate)
#                                     |> List.head
#                                     |> Maybe.withDefault ""
#                         in
#                         { text = text
#                         , uiNode = entryUINode
#                         }
#                     )
#                 |> List.sortBy (.uiNode >> .totalDisplayRegion >> .y)
#     in
#     { uiNode = contextMenuUINode
#     , entries = entries
#     }


def parseShipUIFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[ShipUI]:
    pass
# parseShipUIFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe ShipUI
# parseShipUIFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ShipUI")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just shipUINode ->
#             case
#                 shipUINode
#                     |> listDescendantsWithDisplayRegion
#                     |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "CapacitorContainer")
#                     |> List.head
#             of
#                 Nothing ->
#                     Nothing
#                 Just capacitorUINode ->
#                     let
#                         descendantNodesFromPythonObjectTypeNameEqual pythonObjectTypeName =
#                             shipUINode
#                                 |> listDescendantsWithDisplayRegion
#                                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) pythonObjectTypeName)
#                         capacitor =
#                             capacitorUINode |> parseShipUICapacitorFromUINode
#                         {-
#                            speedGaugeElement =
#                                shipUINode
#                                    |> listDescendantsWithDisplayRegion
#                                    |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SpeedGauge")
#                                    |> List.head
#                         -}
#                         maybeIndicationNode =
#                             shipUINode
#                                 |> listDescendantsWithDisplayRegion
#                                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map (str.toLower >> str.contains "indicationcontainer") >> Maybe.withDefault False)
#                                 |> List.head
#                         indication =
#                             maybeIndicationNode
#                                 |> Maybe.map (parseShipUIIndication >> Just)
#                                 |> Maybe.withDefault Nothing
#                         moduleButtons =
#                             shipUINode
#                                 |> listDescendantsWithDisplayRegion
#                                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ShipSlot")
#                                 |> List.filterMap
#                                     (\slotNode ->
#                                         slotNode
#                                             |> listDescendantsWithDisplayRegion
#                                             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ModuleButton")
#                                             |> List.head
#                                             |> Maybe.map
#                                                 (\moduleButtonNode ->
#                                                     parseShipUIModuleButton { slotNode = slotNode, moduleButtonNode = moduleButtonNode }
#                                                 )
#                                     )
#                         getLastValuePercentFromGaugeName gaugeName =
#                             shipUINode
#                                 |> listDescendantsWithDisplayRegion
#                                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map ((==) gaugeName) >> Maybe.withDefault False)
#                                 |> List.head
#                                 |> Maybe.andThen (.uiNode >> .dictEntriesOfinterest >> Dict.get "_lastValue")
#                                 |> Maybe.andThen (Json.Decode.decodeValue Json.Decode.float >> Result.toMaybe)
#                                 |> Maybe.map ((*) 100 >> round)
#                         maybeHitpointsPercent =
#                             case ( getLastValuePercentFromGaugeName "structureGauge", getLastValuePercentFromGaugeName "armorGauge", getLastValuePercentFromGaugeName "shieldGauge" ) of
#                                 ( Just structure, Just armor, Just shield ) ->
#                                     Just { structure = structure, armor = armor, shield = shield }
#                                 _ ->
#                                     Nothing
#                         offensiveBuffButtonNames =
#                             shipUINode
#                                 |> listDescendantsWithDisplayRegion
#                                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "OffensiveBuffButton")
#                                 |> List.filterMap (.uiNode >> getNameFromDictEntries)
#                         squadronsUI =
#                             shipUINode
#                                 |> listDescendantsWithDisplayRegion
#                                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SquadronsUI")
#                                 |> List.head
#                                 |> Maybe.map parseSquadronsUI
#                     in
#                     maybeHitpointsPercent
#                         |> Maybe.map
#                             (\hitpointsPercent ->
#                                 { uiNode = shipUINode
#                                 , capacitor = capacitor
#                                 , hitpointsPercent = hitpointsPercent
#                                 , indication = indication
#                                 , moduleButtons = moduleButtons
#                                 , moduleButtonsRows = groupShipUIModulesintoRows capacitor moduleButtons
#                                 , offensiveBuffButtonNames = offensiveBuffButtonNames
#                                 , squadronsUI = squadronsUI
#                                 , stopButton = descendantNodesFromPythonObjectTypeNameEqual "StopButton" |> List.head
#                                 , maxSpeedButton = descendantNodesFromPythonObjectTypeNameEqual "MaxSpeedButton" |> List.head
#                                 }
#                             )


def parseShipUIModuleButton(slotNode: UITreeNodeWithDisplayRegion, moduleButtonNode: UITreeNodeWithDisplayRegion) -> ShipUIModuleButton:
    pass
# parseShipUIModuleButton : { slotNode : UITreeNodeWithDisplayRegion, moduleButtonNode : UITreeNodeWithDisplayRegion } -> ShipUIModuleButton
# parseShipUIModuleButton { slotNode, moduleButtonNode } =
#     let
#         rotationFloatFromRampName rampName =
#             slotNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> (==) (Just rampName))
#                 |> List.filterMap (.uiNode >> getRotationFloatFromDictEntries)
#                 |> List.head
#         rampRotationMilli =
#             case ( rotationFloatFromRampName "leftRamp", rotationFloatFromRampName "rightRamp" ) of
#                 ( Just leftRampRotationFloat, Just rightRampRotationFloat ) ->
#                     if
#                         (leftRampRotationFloat < 0 || pi * 2.01 < leftRampRotationFloat)
#                             || (rightRampRotationFloat < 0 || pi * 2.01 < rightRampRotationFloat)
#                     then
#                         Nothing
#                     else
#                         Just (max 0 (min 1000 (round (1000 - ((leftRampRotationFloat + rightRampRotationFloat) * 500) / pi))))
#                 _ ->
#                     Nothing
#     in
#     { uiNode = moduleButtonNode
#     , slotUINode = slotNode
#     , isActive =
#         moduleButtonNode.uiNode.dictEntriesOfinterest
#             |> Dict.get "ramp_active"
#             |> Maybe.andThen (Json.Decode.decodeValue Json.Decode.bool >> Result.toMaybe)
#     , isHiliteVisible =
#         slotNode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "Sprite")
#             |> List.filter (.uiNode >> getNameFromDictEntries >> (==) (Just "hilite"))
#             |> List.isEmpty
#             |> not
#     , rampRotationMilli = rampRotationMilli
#     }


def parseShipUICapacitorFromUINode(capacitorUINode: UITreeNodeWithDisplayRegion) -> ShipUICapacitor:
    pass
# parseShipUICapacitorFromUINode : UITreeNodeWithDisplayRegion -> ShipUICapacitor
# parseShipUICapacitorFromUINode capacitorUINode =
#     let
#         pmarks =
#             capacitorUINode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map ((==) "pmark") >> Maybe.withDefault False)
#                 |> List.map
#                     (\pmarkUINode ->
#                         { uiNode = pmarkUINode
#                         , colorPercent = pmarkUINode.uiNode |> getColorPercentFromDictEntries
#                         }
#                     )
#         maybePmarksFills =
#             pmarks
#                 |> List.map (.colorPercent >> Maybe.map (\colorPercent -> colorPercent.a < 20))
#                 |> Maybe.Extra.combine
#         levelFromPmarksPercent =
#             maybePmarksFills
#                 |> Maybe.andThen
#                     (\pmarksFills ->
#                         if (pmarksFills |> List.length) < 1 then
#                             Nothing
#                         else
#                             Just (((pmarksFills |> List.filter identity |> List.length) * 100) // (pmarksFills |> List.length))
#                     )
#     in
#     { uiNode = capacitorUINode
#     , pmarks = pmarks
#     , levelFromPmarksPercent = levelFromPmarksPercent
#     }


def groupShipUIModulesintoRows(capacitor: ShipUICapacitor, modules: List[ShipUIModuleButton]) -> ModuleRows:

    verticalDistanceThreshold = 20

    def verticalCenterOfUINode(uiNode: UITreeNodeWithDisplayRegion) -> int:
        return uiNode.totalDisplayRegion.y + uiNode.totalDisplayRegion.height / 2
    capacitorVerticalCenter = verticalCenterOfUINode(capacitor.uiNode)

    def foldFunction(shipModule: ShipUIModuleButton, previousRows: ModuleRows):
        if verticalCenterOfUINode(shipModule.uiNode) < (capacitorVerticalCenter - verticalDistanceThreshold):
            previousRows.top.append(shipModule)
        elif verticalCenterOfUINode(shipModule.uiNode) > (capacitorVerticalCenter + verticalDistanceThreshold):
            previousRows.bottom.append(shipModule)
        else:
            previousRows.middle.append(shipModule)
    _modules = ModuleRows([], [], [])
    foldr(foldFunction, _modules, modules)
    return _modules
# groupShipUIModulesintoRows :
#     ShipUICapacitor
#     -> List ShipUIModuleButton
#     -> { top : List ShipUIModuleButton, middle : List ShipUIModuleButton, bottom : List ShipUIModuleButton }
# groupShipUIModulesintoRows capacitor modules =
#     let
#         verticalDistanceThreshold =
#             20
#         verticalCenterOfUINode uiNode =
#             uiNode.totalDisplayRegion.y + uiNode.totalDisplayRegion.height // 2
#         capacitorVerticalCenter =
#             verticalCenterOfUINode capacitor.uiNode
#     in
#     modules
#         |> List.foldr
#             (\shipModule previousRows ->
#                 if verticalCenterOfUINode shipModule.uiNode < capacitorVerticalCenter - verticalDistanceThreshold then
#                     { previousRows | top = shipModule :: previousRows.top }
#                 else if verticalCenterOfUINode shipModule.uiNode > capacitorVerticalCenter + verticalDistanceThreshold then
#                     { previousRows | bottom = shipModule :: previousRows.bottom }
#                 else
#                     { previousRows | middle = shipModule :: previousRows.middle }
#             )
#             { top = [], middle = [], bottom = [] }


def parseShipIndication(indicationUINode: UITreeNodeWithDisplayRegion) -> ShipUIIndication:
    pass
# parseShipUIIndication : UITreeNodeWithDisplayRegion -> ShipUIIndication
# parseShipUIIndication indicationUINode =
#     let
#         displayTexts =
#             indicationUINode.uiNode |> getAllContainedDisplayTexts
#         maneuverType =
#             [ ( "Warp", ManeuverWarp )
#             , ( "Jump", ManeuverJump )
#             , ( "Orbit", ManeuverOrbit )
#             , ( "Approach", ManeuverApproach )
#             -- Sample `session-2022-05-23T23-00-32-87ba97.zip` shared by Abaddon at https://forum.botlab.org/t/i-want-to-add-korean-support-on-eve-online-bot-what-should-i-do/4370/9
#             , ( "워프 드라이브 가동", ManeuverWarp )
#             -- Sample `session-2022-05-26T03-13-42-83df2b.zip` shared by Abaddon at https://forum.botlab.org/t/i-want-to-add-korean-support-on-eve-online-bot-what-should-i-do/4370/14
#             , ( "점프 중", ManeuverJump )
#             ]
#                 |> List.filterMap
#                     (\( pattern, candidateManeuverType ) ->
#                         if displayTexts |> List.any (str.contains pattern) then
#                             Just candidateManeuverType
#                         else
#                             Nothing
#                     )
#                 |> List.head
#     in
#     { uiNode = indicationUINode, maneuverType = maneuverType }


def parseSquadronsUI(squadronsUINode: UITreeNodeWithDisplayRegion) -> SquadronsUI:
    pass
# parseSquadronsUI : UITreeNodeWithDisplayRegion -> SquadronsUI
# parseSquadronsUI squadronsUINode =
#     { uiNode = squadronsUINode
#     , squadrons =
#         squadronsUINode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SquadronUI")
#             |> List.map parseSquadronUI
#     }


def parseSquadronUI(squadronUINode: UITreeNodeWithDisplayRegion) -> SquadronUI:
    pass
# parseSquadronUI : UITreeNodeWithDisplayRegion -> SquadronUI
# parseSquadronUI squadronUINode =
#     { uiNode = squadronUINode
#     , abilities =
#         squadronUINode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "AbilityIcon")
#             |> List.map parseSquadronAbilityIcon
#     , actionLabel =
#         squadronUINode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SquadronActionLabel")
#             |> List.head
#     }


def parseSquadronAbilityIcon(abilityIconUINode: UITreeNodeWithDisplayRegion) -> SquadronAbilityIcon:
    pass
# parseSquadronAbilityIcon : UITreeNodeWithDisplayRegion -> SquadronAbilityIcon
# parseSquadronAbilityIcon abilityIconUINode =
#     { uiNode = abilityIconUINode
#     , quantity =
#         abilityIconUINode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map (str.toLower >> str.contains "quantity") >> Maybe.withDefault False)
#             |> List.concatMap (.uiNode >> getAllContainedDisplayTexts)
#             |> List.head
#             |> Maybe.andThen (str.trim >> str.toint)
#     , ramp_active =
#         abilityIconUINode.uiNode.dictEntriesOfinterest
#             |> Dict.get "ramp_active"
#             |> Maybe.andThen (Json.Decode.decodeValue Json.Decode.bool >> Result.toMaybe)
#     }


def parseTargetsFromUITreeRoot(x: UITreeNodeWithDisplayRegion) -> List[Target]:
    pass
# parseTargetsFromUITreeRoot : UITreeNodeWithDisplayRegion -> List Target
# parseTargetsFromUITreeRoot =
#     listDescendantsWithDisplayRegion
#         >> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "TargetInBar")
#         >> List.map parseTarget


def parseTarget(targetNode: UITreeNodeWithDisplayRegion) -> Target:
    pass
# parseTarget : UITreeNodeWithDisplayRegion -> Target
# parseTarget targetNode =
#     let
#         textsTopToBottom =
#             targetNode
#                 |> getAllContainedDisplayTextsWithRegion
#                 |> List.sortBy (Tuple.second >> .totalDisplayRegion >> .y)
#                 |> List.map Tuple.first
#         barAndImageCont =
#             targetNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> (==) (Just "barAndImageCont"))
#                 |> List.head
#         isActiveTarget =
#             targetNode.uiNode
#                 |> listDescendantsInUITreeNode
#                 |> List.any (.pythonObjectTypeName >> (==) "ActiveTargetOnBracket")
#         assignedContainerNode =
#             targetNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map (str.toLower >> str.contains "assigned") >> Maybe.withDefault False)
#                 |> List.sortBy (.totalDisplayRegion >> .width)
#                 |> List.head
#         assignedIcons =
#             assignedContainerNode
#                 |> Maybe.map listDescendantsWithDisplayRegion
#                 |> Maybe.withDefault []
#                 |> List.filter (\uiNode -> [ "Sprite", "Icon" ] |> List.member uiNode.uiNode.pythonObjectTypeName)
#     in
#     { uiNode = targetNode
#     , barAndImageCont = barAndImageCont
#     , textsTopToBottom = textsTopToBottom
#     , isActiveTarget = isActiveTarget
#     , assignedContainerNode = assignedContainerNode
#     , assignedIcons = assignedIcons
#     }


def parseOverviewWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[OverviewWindow]:
    pass
# parseOverviewWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe OverviewWindow
# parseOverviewWindowFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "OverView")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just overviewWindowNode ->
#             let
#                 scrollNode =
#                     overviewWindowNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> str.toLower >> str.contains "scroll")
#                         |> List.head
#                 scrollControlsNode =
#                     scrollNode
#                         |> Maybe.map listDescendantsWithDisplayRegion
#                         |> Maybe.withDefault []
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "ScrollControls")
#                         |> List.head
#                 headersContainerNode =
#                     scrollNode
#                         |> Maybe.map listDescendantsWithDisplayRegion
#                         |> Maybe.withDefault []
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> str.toLower >> str.contains "headers")
#                         |> List.head
#                 entriesHeaders =
#                     headersContainerNode
#                         |> Maybe.map getAllContainedDisplayTextsWithRegion
#                         |> Maybe.withDefault []
#                 entries =
#                     overviewWindowNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "OverviewScrollEntry")
#                         |> List.map (parseOverviewWindowEntry entriesHeaders)
#             in
#             Just
#                 { uiNode = overviewWindowNode
#                 , entriesHeaders = entriesHeaders
#                 , entries = entries
#                 , scrollControls = scrollControlsNode |> Maybe.map parseScrollControls
#                 }


def parseOverviewWindowEntry(entriesHeaders: List[Union[str, UITreeNodeWithDisplayRegion]]) -> Callable[[UITreeNodeWithDisplayRegion], OverviewWindowEntry]:
    def fn(x: UITreeNodeWithDisplayRegion) -> OverviewWindowEntry:
        pass
    return fn
# parseOverviewWindowEntry : List ( str, UITreeNodeWithDisplayRegion ) -> UITreeNodeWithDisplayRegion -> OverviewWindowEntry
# parseOverviewWindowEntry entriesHeaders overviewEntryNode =
#     let
#         textsLeftToRight =
#             overviewEntryNode
#                 |> getAllContainedDisplayTextsWithRegion
#                 |> List.sortBy (Tuple.second >> .totalDisplayRegion >> .x)
#                 |> List.map Tuple.first
#         cellsTexts =
#             overviewEntryNode
#                 |> getAllContainedDisplayTextsWithRegion
#                 |> List.filterMap
#                     (\( cellText, cell ) ->
#                         let
#                             cellMiddle =
#                                 cell.totalDisplayRegion.x + (cell.totalDisplayRegion.width // 2)
#                             maybeHeader =
#                                 entriesHeaders
#                                     |> List.filter
#                                         (\( _, header ) ->
#                                             header.totalDisplayRegion.x
#                                                 < cellMiddle
#                                                 + 1
#                                                 && cellMiddle
#                                                 < header.totalDisplayRegion.x
#                                                 + header.totalDisplayRegion.width
#                                                 - 1
#                                         )
#                                     |> List.head
#                         in
#                         maybeHeader
#                             |> Maybe.map (\( headerText, _ ) -> ( headerText, cellText ))
#                     )
#                 |> Dict.fromList
#         objectDistance =
#             cellsTexts
#                 |> Dict.get "Distance"
#         objectDistanceInMeters =
#             objectDistance
#                 |> Maybe.map parseOverviewEntryDistanceInMetersFromText
#                 |> Maybe.withDefault (Err "Did not find the 'Distance' cell text.")
#         spaceObjectIconNode =
#             overviewEntryNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SpaceObjectIcon")
#                 |> List.head
#         iconSpriteColorPercent =
#             spaceObjectIconNode
#                 |> Maybe.map listDescendantsWithDisplayRegion
#                 |> Maybe.withDefault []
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> (==) (Just "iconSprite"))
#                 |> List.head
#                 |> Maybe.andThen (.uiNode >> getColorPercentFromDictEntries)
#         namesUnderSpaceObjectIcon =
#             spaceObjectIconNode
#                 |> Maybe.map (.uiNode >> listDescendantsInUITreeNode)
#                 |> Maybe.withDefault []
#                 |> List.filterMap getNameFromDictEntries
#                 |> Set.fromList
#         bgColorFillsPercent =
#             overviewEntryNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "Fill")
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map ((==) "bgColor") >> Maybe.withDefault False)
#                 |> List.filterMap (\fillUiNode -> fillUiNode.uiNode |> getColorPercentFromDictEntries)
#         rightAlignedIconsHints =
#             overviewEntryNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map ((==) "rightAlignedIconContainer") >> Maybe.withDefault False)
#                 |> List.concatMap listDescendantsWithDisplayRegion
#                 |> List.filterMap (.uiNode >> getHintTextFromDictEntries)
#         rightAlignedIconsHintsContainsTextIgnoringCase textToSearch =
#             rightAlignedIconsHints |> List.any (str.toLower >> str.contains (textToSearch |> str.toLower))
#         commonIndications =
#             { targeting = namesUnderSpaceObjectIcon |> Set.member "targeting"
#             , targetedByMe = namesUnderSpaceObjectIcon |> Set.member "targetedByMeIndicator"
#             , isJammingMe = rightAlignedIconsHintsContainsTextIgnoringCase "is jamming me"
#             , isWarpDisruptingMe = rightAlignedIconsHintsContainsTextIgnoringCase "is warp disrupting me"
#             }
#     in
#     { uiNode = overviewEntryNode
#     , textsLeftToRight = textsLeftToRight
#     , cellsTexts = cellsTexts
#     , objectDistance = objectDistance
#     , objectDistanceInMeters = objectDistanceInMeters
#     , objectName = cellsTexts |> Dict.get "Name"
#     , objectType = cellsTexts |> Dict.get "Type"
#     , objectAlliance = cellsTexts |> Dict.get "Alliance"
#     , iconSpriteColorPercent = iconSpriteColorPercent
#     , namesUnderSpaceObjectIcon = namesUnderSpaceObjectIcon
#     , bgColorFillsPercent = bgColorFillsPercent
#     , rightAlignedIconsHints = rightAlignedIconsHints
#     , commonIndications = commonIndications
#     }


def parseOverviewEntryDistanceInMetersFromText(distanceDisplayTextBeforeTrim: str) -> Union[str, int]:
    pass
# parseOverviewEntryDistanceInMetersFromText : str -> Result str int
# parseOverviewEntryDistanceInMetersFromText distanceDisplayTextBeforeTrim =
#     case distanceDisplayTextBeforeTrim |> str.trim |> str.split " " |> List.reverse of
#         unitText :: reversedNumberTexts ->
#             case parseDistanceUnitInMeters unitText of
#                 Nothing ->
#                     Err ("Failed to parse distance unit text of '" ++ unitText ++ "'")
#                 Just unitInMeters ->
#                     case
#                         reversedNumberTexts |> List.reverse |> str.join " " |> parseNumberTruncatingAfterOptionalDecimalSeparator
#                     of
#                         Err parseNumberError ->
#                             Err ("Failed to parse number: " ++ parseNumberError)
#                         Ok parsedNumber ->
#                             Ok (parsedNumber * unitInMeters)
#         _ ->
#             Err "Expecting at least one whitespace character separating number and unit."


def parseDistanceUnitInMeters(unitText: str) -> Optional[int]:
    pass
# parseDistanceUnitInMeters : str -> Maybe int
# parseDistanceUnitInMeters unitText =
#     case str.trim unitText of
#         "m" ->
#             Just 1
#         "km" ->
#             Just 1000
#         _ ->
#             Nothing


def parseSelectedItemWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[SelectedItemWindow]:
    pass
# parseSelectedItemWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe SelectedItemWindow
# parseSelectedItemWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ActiveItem")
#         |> List.head
#         |> Maybe.map parseSelectedItemWindow


def parseSelectedItemWindow(windowNode: UITreeNodeWithDisplayRegion) -> SelectedItemWindow:
    pass
# parseSelectedItemWindow : UITreeNodeWithDisplayRegion -> SelectedItemWindow
# parseSelectedItemWindow windowNode =
#     let
#         actionButtonFromTexturePathEnding texturePathEnding =
#             windowNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter
#                     (.uiNode
#                         >> getTexturePathFromDictEntries
#                         >> Maybe.map (str.toLower >> str.endsWith (str.toLower texturePathEnding))
#                         >> Maybe.withDefault False
#                     )
#                 |> List.head
#         orbitButton =
#             actionButtonFromTexturePathEnding "44_32_21.png"
#     in
#     { uiNode = windowNode, orbitButton = orbitButton }


def parseDronesWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[DronesWindow]:
    pass
# parseDronesWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe DronesWindow
# parseDronesWindowFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "DroneView")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just windowNode ->
#             let
#                 {-
#                    scrollNode =
#                        windowNode
#                            |> listDescendantsWithDisplayRegion
#                            |> List.filter (.uiNode >> .pythonObjectTypeName >> str.toLower >> str.contains "scroll")
#                            |> List.head
#                 -}
#                 droneGroupHeaders =
#                     windowNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "Group")
#                         |> List.filterMap parseDronesWindowDroneGroupHeader
#                 droneEntries =
#                     windowNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "DroneEntry")
#                         |> List.map parseDronesWindowDroneEntry
#                 droneGroups =
#                     [ droneEntries |> List.map DronesWindowEntryDrone
#                     , droneGroupHeaders
#                         |> List.map (\header -> { header = header, children = [] })
#                         |> List.map DronesWindowEntryGroup
#                     ]
#                         |> List.concat
#                         |> dronesGroupTreesFromFlatListOfEntries
#                 droneGroupFromHeaderTextPart headerTextPart =
#                     droneGroups
#                         |> List.filter (.header >> .maintext >> Maybe.withDefault "" >> str.toLower >> str.contains (headerTextPart |> str.toLower))
#                         |> List.sortBy (.header >> .maintext >> Maybe.map str.length >> Maybe.withDefault 999)
#                         |> List.head
#             in
#             Just
#                 { uiNode = windowNode
#                 , droneGroups = droneGroups
#                 , droneGroupInBay = droneGroupFromHeaderTextPart "in Bay"
#                 , droneGroupInLocalSpace = droneGroupFromHeaderTextPart "in local space"
#                 }


def dronesGroupTreesFromFlatListOfEntries(entriesBeforeOrdering: List[Union[DronesWindowEntryGroup, DronesWindowEntryDrone]]) -> List[DronesWindowEntryGroupStructure]:
    pass
# dronesGroupTreesFromFlatListOfEntries : List DronesWindowEntry -> List DronesWindowEntryGroupStructure
# dronesGroupTreesFromFlatListOfEntries entriesBeforeOrdering =
#     let
#         verticalOffsetFromEntry entry =
#             case entry of
#                 DronesWindowEntryDrone droneEntry ->
#                     droneEntry.uiNode.totalDisplayRegion.y
#                 DronesWindowEntryGroup groupEntry ->
#                     groupEntry.header.uiNode.totalDisplayRegion.y
#         entriesOrderedVertically =
#             entriesBeforeOrdering
#                 |> List.sortBy verticalOffsetFromEntry
#     in
#     entriesOrderedVertically
#         |> List.filterMap
#             (\entry ->
#                 case entry of
#                     DronesWindowEntryDrone _ ->
#                         Nothing
#                     DronesWindowEntryGroup group ->
#                         Just group
#             )
#         |> List.head
#         |> Maybe.map
#             (\topmostGroupEntry ->
#                 let
#                     entriesUpToSibling =
#                         entriesOrderedVertically
#                             |> List.Extra.dropWhile
#                                 (verticalOffsetFromEntry
#                                     >> (\offset -> offset <= verticalOffsetFromEntry (DronesWindowEntryGroup topmostGroupEntry))
#                                 )
#                             |> List.Extra.takeWhile
#                                 (\entry ->
#                                     case entry of
#                                         DronesWindowEntryDrone _ ->
#                                             True
#                                         DronesWindowEntryGroup group ->
#                                             topmostGroupEntry.header.expander.uiNode.totalDisplayRegion.x
#                                                 < (group.header.expander.uiNode.totalDisplayRegion.x - 3)
#                                 )
#                     childGroupTrees =
#                         dronesGroupTreesFromFlatListOfEntries entriesUpToSibling
#                     childDrones =
#                         entriesUpToSibling
#                             |> List.Extra.takeWhile
#                                 (\entry ->
#                                     case entry of
#                                         DronesWindowEntryDrone _ ->
#                                             True
#                                         DronesWindowEntryGroup _ ->
#                                             False
#                                 )
#                     children =
#                         [ childDrones, childGroupTrees |> List.map DronesWindowEntryGroup ]
#                             |> List.concat
#                             |> List.sortBy verticalOffsetFromEntry
#                     topmostGroupTree =
#                         { header = topmostGroupEntry.header
#                         , children = children
#                         }
#                     bottommostDescendantOffset =
#                         enumerateDescendantsOfDronesGroup topmostGroupTree
#                             |> List.map verticalOffsetFromEntry
#                             |> List.maximum
#                             |> Maybe.withDefault (verticalOffsetFromEntry (DronesWindowEntryGroup topmostGroupTree))
#                     entriesBelow =
#                         entriesOrderedVertically
#                             |> List.Extra.dropWhile (verticalOffsetFromEntry >> (\offset -> offset <= bottommostDescendantOffset))
#                 in
#                 topmostGroupTree :: dronesGroupTreesFromFlatListOfEntries entriesBelow
#             )
#         |> Maybe.withDefault []


def enumerateAllDronesFromDronesGroup(x: DronesWindowEntryGroupStructure) -> List[DronesWindowEntryDroneStructure]:
    pass
# enumerateAllDronesFromDronesGroup : DronesWindowEntryGroupStructure -> List DronesWindowEntryDroneStructure
# enumerateAllDronesFromDronesGroup =
#     enumerateDescendantsOfDronesGroup
#         >> List.filterMap
#             (\entry ->
#                 case entry of
#                     DronesWindowEntryDrone drone ->
#                         Just drone
#                     DronesWindowEntryGroup _ ->
#                         Nothing
#             )


def enumerateDescendantsOfDronesGroup(group: DronesWindowEntryGroupStructure) -> List[Union[DronesWindowEntryGroup, DronesWindowEntryDrone]]:
    pass
# enumerateDescendantsOfDronesGroup : DronesWindowEntryGroupStructure -> List DronesWindowEntry
# enumerateDescendantsOfDronesGroup group =
#     group.children
#         |> List.concatMap
#             (\child ->
#                 case child of
#                     DronesWindowEntryDrone _ ->
#                         [ child ]
#                     DronesWindowEntryGroup childGroup ->
#                         child :: enumerateDescendantsOfDronesGroup childGroup
#             )


def parseDronesWindowDroneGroupHeader(groupHeaderUiNode: UITreeNodeWithDisplayRegion) -> Optional[DronesWindowDroneGroupHeader]:
    pass
# parseDronesWindowDroneGroupHeader : UITreeNodeWithDisplayRegion -> Maybe DronesWindowDroneGroupHeader
# parseDronesWindowDroneGroupHeader groupHeaderUiNode =
#     case
#         groupHeaderUiNode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter
#                 (.uiNode
#                     >> getNameFromDictEntries
#                     >> (Maybe.map (str.toLower >> str.contains "expander") >> Maybe.withDefault False)
#                 )
#     of
#         [ expanderNode ] ->
#             let
#                 maintext =
#                     groupHeaderUiNode
#                         |> getAllContainedDisplayTextsWithRegion
#                         |> List.sortBy (Tuple.second >> .totalDisplayRegion >> areaFromDisplayRegion >> Maybe.withDefault 0)
#                         |> List.map Tuple.first
#                         |> List.head
#                 quantityFromTitle =
#                     maintext |> Maybe.andThen (parseQuantityFromDroneGroupTitleText >> Result.withDefault Nothing)
#             in
#             Just
#                 { uiNode = groupHeaderUiNode
#                 , maintext = maintext
#                 , expander = expanderNode |> parseExpander
#                 , quantityFromTitle = quantityFromTitle
#                 }
#         _ ->
#             Nothing


def parseQuantityFromDroneGroupTitleText(droneGroupTitleText: str) -> Optional[Union[str, int]]:
    pass
# parseQuantityFromDroneGroupTitleText : str -> Result str (Maybe int)
# parseQuantityFromDroneGroupTitleText droneGroupTitleText =
#     case droneGroupTitleText |> str.split "(" |> List.drop 1 of
#         [] ->
#             Ok Nothing
#         [ textAfterOpeningParenthesis ] ->
#             textAfterOpeningParenthesis
#                 |> str.split ")"
#                 |> List.head
#                 |> Maybe.andThen (str.trim >> str.toint)
#                 |> Result.fromMaybe ("Failed to parse to integer from '" ++ textAfterOpeningParenthesis ++ "'")
#                 |> Result.map Just
#         _ ->
#             Err "Found unexpected number of parentheses."


def parseDronesWindowDroneEntry(droneEntryNode: UITreeNodeWithDisplayRegion) -> DronesWindowEntryDroneStructure:
    pass
# parseDronesWindowDroneEntry : UITreeNodeWithDisplayRegion -> DronesWindowEntryDroneStructure
# parseDronesWindowDroneEntry droneEntryNode =
#     let
#         maintext =
#             droneEntryNode
#                 |> getAllContainedDisplayTextsWithRegion
#                 |> List.sortBy (Tuple.second >> .totalDisplayRegion >> areaFromDisplayRegion >> Maybe.withDefault 0)
#                 |> List.map Tuple.first
#                 |> List.head
#         gaugeValuePercentFromContainerName containerName =
#             droneEntryNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> (==) (Just containerName))
#                 |> List.head
#                 |> Maybe.andThen
#                     (\gaugeNode ->
#                         let
#                             gaudeDescendantFromName gaugeDescendantName =
#                                 gaugeNode
#                                     |> listDescendantsWithDisplayRegion
#                                     |> List.filter (.uiNode >> getNameFromDictEntries >> (==) (Just gaugeDescendantName))
#                                     |> List.head
#                         in
#                         gaudeDescendantFromName "droneGaugeBar"
#                             |> Maybe.andThen
#                                 (\gaugeBar ->
#                                     gaudeDescendantFromName "droneGaugeBarDmg"
#                                         |> Maybe.map
#                                             (\droneGaugeBarDmg ->
#                                                 ((gaugeBar.totalDisplayRegion.width - droneGaugeBarDmg.totalDisplayRegion.width) * 100)
#                                                     // gaugeBar.totalDisplayRegion.width
#                                             )
#                                 )
#                     )
#         hitpointsPercent =
#             gaugeValuePercentFromContainerName "gauge_shield"
#                 |> Maybe.andThen
#                     (\shieldPercent ->
#                         gaugeValuePercentFromContainerName "gauge_armor"
#                             |> Maybe.andThen
#                                 (\armorPercent ->
#                                     gaugeValuePercentFromContainerName "gauge_struct"
#                                         |> Maybe.map
#                                             (\structPercent ->
#                                                 { shield = shieldPercent
#                                                 , armor = armorPercent
#                                                 , structure = structPercent
#                                                 }
#                                             )
#                                 )
#                     )
#     in
#     { uiNode = droneEntryNode
#     , maintext = maintext
#     , hitpointsPercent = hitpointsPercent
#     }


def parseProbeScannerWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[ProbeScannerWindow]:
    pass
# parseProbeScannerWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe ProbeScannerWindow
# parseProbeScannerWindowFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ProbeScannerWindow")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just windowNode ->
#             let
#                 scanResultsNodes =
#                     windowNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ScanResultNew")
#                 scrollNode =
#                     windowNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map (str.contains "ResultsContainer") >> Maybe.withDefault False)
#                         |> List.concatMap listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> str.toLower >> str.contains "scroll")
#                         |> List.head
#                 headersContainerNode =
#                     scrollNode
#                         |> Maybe.map listDescendantsWithDisplayRegion
#                         |> Maybe.withDefault []
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> str.toLower >> str.contains "header")
#                         |> List.head
#                 entriesHeaders =
#                     headersContainerNode
#                         |> Maybe.map getAllContainedDisplayTextsWithRegion
#                         |> Maybe.withDefault []
#                 scanResults =
#                     scanResultsNodes
#                         |> List.map (parseProbeScanResult entriesHeaders)
#             in
#             Just { uiNode = windowNode, scanResults = scanResults }


def parseProbeScanResult(entriesHeaders: List[Union[str, UITreeNodeWithDisplayRegion]]) -> Callable[[UITreeNodeWithDisplayRegion], ProbeScanResult]:
    def fn(x: UITreeNodeWithDisplayRegion) -> ProbeScanResult:
        pass
    return fn
# parseProbeScanResult : List ( str, UITreeNodeWithDisplayRegion ) -> UITreeNodeWithDisplayRegion -> ProbeScanResult
# parseProbeScanResult entriesHeaders scanResultNode =
#     let
#         textsLeftToRight =
#             scanResultNode
#                 |> getAllContainedDisplayTextsWithRegion
#                 |> List.sortBy (Tuple.second >> .totalDisplayRegion >> .x)
#                 |> List.map Tuple.first
#         cellsTexts =
#             scanResultNode
#                 |> getAllContainedDisplayTextsWithRegion
#                 |> List.filterMap
#                     (\( cellText, cell ) ->
#                         let
#                             cellMiddle =
#                                 cell.totalDisplayRegion.x + (cell.totalDisplayRegion.width // 2)
#                             maybeHeader =
#                                 entriesHeaders
#                                     |> List.filter
#                                         (\( _, header ) ->
#                                             header.totalDisplayRegion.x
#                                                 < cellMiddle
#                                                 + 1
#                                                 && cellMiddle
#                                                 < header.totalDisplayRegion.x
#                                                 + header.totalDisplayRegion.width
#                                                 - 1
#                                         )
#                                     |> List.head
#                         in
#                         maybeHeader
#                             |> Maybe.map (\( headerText, _ ) -> ( headerText, cellText ))
#                     )
#                 |> Dict.fromList
#         warpButton =
#             scanResultNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getTexturePathFromDictEntries >> Maybe.map (str.endsWith "44_32_18.png") >> Maybe.withDefault False)
#                 |> List.head
#     in
#     { uiNode = scanResultNode
#     , textsLeftToRight = textsLeftToRight
#     , cellsTexts = cellsTexts
#     , warpButton = warpButton
#     }


def parseDirectionalScannerWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[DirectionalScannerWindow]:
    pass
# parseDirectionalScannerWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe DirectionalScannerWindow
# parseDirectionalScannerWindowFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "DirectionalScanner")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just windowNode ->
#             let
#                 scrollNode =
#                     windowNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> str.toLower >> str.contains "scroll")
#                         |> List.sortBy (.totalDisplayRegion >> areaFromDisplayRegion >> Maybe.withDefault 0 >> negate)
#                         |> List.head
#                 scanResultsNodes =
#                     scrollNode
#                         |> Maybe.map listDescendantsWithDisplayRegion
#                         |> Maybe.withDefault []
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "DirectionalScanResultEntry")
#             in
#             Just
#                 { uiNode = windowNode
#                 , scrollNode = scrollNode
#                 , scanResults = scanResultsNodes
#                 }


def parseStationWindowFromUITreeRoot(uiTreeroot: UITreeNodeWithDisplayRegion) -> Optional[StationWindow]:
    parseShipUICapacitorFromUINode
# parseStationWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe StationWindow
# parseStationWindowFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "LobbyWnd")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just windowNode ->
#             let
#                 buttons =
#                     windowNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "Button")
#                 buttonFromDisplayText textToSearch =
#                     let
#                         textToSearchLowercase =
#                             str.toLower textToSearch
#                         textMatches text =
#                             text == textToSearchLowercase || (text |> str.contains (">" ++ textToSearchLowercase ++ "<"))
#                     in
#                     buttons
#                         |> List.filter (.uiNode >> getAllContainedDisplayTexts >> List.map (str.toLower >> str.trim) >> List.any textMatches)
#                         |> List.head
#             in
#             Just
#                 { uiNode = windowNode
#                 , undockButton = buttonFromDisplayText "undock"
#                 , abortUndockButton = buttonFromDisplayText "undocking"
#                 }


def parseInventoryWindowsFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> List[InventoryWindow]:
    pass
# parseInventoryWindowsFromUITreeRoot : UITreeNodeWithDisplayRegion -> List InventoryWindow
# parseInventoryWindowsFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (\uiNode -> [ "InventoryPrimary", "ActiveShipCargo" ] |> List.member uiNode.uiNode.pythonObjectTypeName)
#         |> List.map parseInventoryWindow


def parseInventoryWindow(windowUiNode: UITreeNodeWithDisplayRegion) -> InventoryWindow:
    pass
# parseInventoryWindow : UITreeNodeWithDisplayRegion -> InventoryWindow
# parseInventoryWindow windowUiNode =
#     let
#         selectedContainerCapacityGaugeNode =
#             windowUiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "CapacityGauge")
#                 |> List.head
#         selectedContainerCapacityGauge =
#             selectedContainerCapacityGaugeNode
#                 |> Maybe.map (.uiNode >> listDescendantsInUITreeNode)
#                 |> Maybe.withDefault []
#                 |> List.filterMap getDisplayText
#                 |> List.sortBy (str.length >> negate)
#                 |> List.head
#                 |> Maybe.map parseInventoryCapacityGaugeText
#         leftTreeEntriesRootNodes =
#             windowUiNode |> getContainedTreeViewEntryRootNodes
#         leftTreeEntries =
#             leftTreeEntriesRootNodes |> List.map parseInventoryWindowTreeViewEntry
#         rightContainerNode =
#             windowUiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter
#                     (\uiNode ->
#                         (uiNode.uiNode.pythonObjectTypeName == "Container")
#                             && (uiNode.uiNode |> getNameFromDictEntries |> Maybe.map (str.contains "right") |> Maybe.withDefault False)
#                     )
#                 |> List.head
#         subCaptionLabelText =
#             rightContainerNode
#                 |> Maybe.map listDescendantsWithDisplayRegion
#                 |> Maybe.withDefault []
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map (str.startsWith "subCaptionLabel") >> Maybe.withDefault False)
#                 |> List.concatMap (.uiNode >> getAllContainedDisplayTexts)
#                 |> List.head
#         maybeSelectedContainerInventoryNode =
#             rightContainerNode
#                 |> Maybe.andThen
#                     (listDescendantsWithDisplayRegion
#                         >> List.filter
#                             (\uiNode ->
#                                 [ "ShipCargo", "ShipDroneBay", "ShipGeneralMiningHold", "StationItems", "ShipFleetHangar", "StructureItemHangar" ]
#                                     |> List.member uiNode.uiNode.pythonObjectTypeName
#                             )
#                         >> List.head
#                     )
#         selectedContainerInventory =
#             maybeSelectedContainerInventoryNode
#                 |> Maybe.map
#                     (\selectedContainerInventoryNode ->
#                         let
#                             listViewItemNodes =
#                                 selectedContainerInventoryNode
#                                     |> listDescendantsWithDisplayRegion
#                                     |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "Item")
#                             scrollControlsNode =
#                                 selectedContainerInventoryNode
#                                     |> listDescendantsWithDisplayRegion
#                                     |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "ScrollControls")
#                                     |> List.head
#                             notListViewItemNodes =
#                                 selectedContainerInventoryNode
#                                     |> listDescendantsWithDisplayRegion
#                                     |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "InvItem")
#                             itemsView =
#                                 if 0 < (listViewItemNodes |> List.length) then
#                                     Just (InventoryItemsListView { items = listViewItemNodes })
#                                 else if 0 < (notListViewItemNodes |> List.length) then
#                                     Just (InventoryItemsNotListView { items = notListViewItemNodes })
#                                 else
#                                     Nothing
#                         in
#                         { uiNode = selectedContainerInventoryNode
#                         , itemsView = itemsView
#                         , scrollControls = scrollControlsNode |> Maybe.map parseScrollControls
#                         }
#                     )
#         buttonToSwitchToListView =
#             rightContainerNode
#                 |> Maybe.map listDescendantsWithDisplayRegion
#                 |> Maybe.withDefault []
#                 |> List.filter
#                     (\uiNode ->
#                         (uiNode.uiNode.pythonObjectTypeName |> str.contains "ButtonIcon")
#                             && ((uiNode.uiNode |> getTexturePathFromDictEntries |> Maybe.withDefault "") |> str.endsWith "38_16_190.png")
#                     )
#                 |> List.head
#     in
#     { uiNode = windowUiNode
#     , leftTreeEntries = leftTreeEntries
#     , subCaptionLabelText = subCaptionLabelText
#     , selectedContainerCapacityGauge = selectedContainerCapacityGauge
#     , selectedContainerInventory = selectedContainerInventory
#     , buttonToSwitchToListView = buttonToSwitchToListView
#     }


def getContainedTreeViewEntryRootNodes(parentNode: UITreeNodeWithDisplayRegion) -> List[UITreeNodeWithDisplayRegion]:
    pass
# getContainedTreeViewEntryRootNodes : UITreeNodeWithDisplayRegion -> List UITreeNodeWithDisplayRegion
# getContainedTreeViewEntryRootNodes parentNode =
#     let
#         leftTreeEntriesAllNodes =
#             parentNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> str.startsWith "TreeViewEntry")
#         isContainedintreeEntry candidate =
#             leftTreeEntriesAllNodes
#                 |> List.concatMap listDescendantsWithDisplayRegion
#                 |> List.member candidate
#     in
#     leftTreeEntriesAllNodes
#         |> List.filter (isContainedintreeEntry >> not)


def parseInventoryWindowTreeViewEntry(treeEntryNode: UITreeNodeWithDisplayRegion) -> InventoryWindowLeftTreeEntry:
    pass
# parseInventoryWindowTreeViewEntry : UITreeNodeWithDisplayRegion -> InventoryWindowLeftTreeEntry
# parseInventoryWindowTreeViewEntry treeEntryNode =
#     let
#         topContNode =
#             treeEntryNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map (str.startsWith "topCont_") >> Maybe.withDefault False)
#                 |> List.sortBy (.totalDisplayRegion >> .y)
#                 |> List.head
#         toggleBtn =
#             topContNode
#                 |> Maybe.map listDescendantsWithDisplayRegion
#                 |> Maybe.withDefault []
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map ((==) "toggleBtn") >> Maybe.withDefault False)
#                 |> List.head
#         text =
#             topContNode
#                 |> Maybe.map getAllContainedDisplayTextsWithRegion
#                 |> Maybe.withDefault []
#                 |> List.sortBy (Tuple.second >> .totalDisplayRegion >> .y)
#                 |> List.head
#                 |> Maybe.map Tuple.first
#                 |> Maybe.withDefault ""
#         childrenNodes =
#             treeEntryNode |> getContainedTreeViewEntryRootNodes
#         children =
#             childrenNodes |> List.map (parseInventoryWindowTreeViewEntry >> InventoryWindowLeftTreeEntryChild)
#     in
#     { uiNode = treeEntryNode
#     , toggleBtn = toggleBtn
#     , selectRegion = topContNode
#     , text = text
#     , children = children
#     }


def unwrapInventoryWindowLeftTreeEntryChild(child: InventoryWindowLeftTreeEntryChild) -> InventoryWindowLeftTreeEntry:
    pass
# unwrapInventoryWindowLeftTreeEntryChild : InventoryWindowLeftTreeEntryChild -> InventoryWindowLeftTreeEntry
# unwrapInventoryWindowLeftTreeEntryChild child =
#     case child of
#         InventoryWindowLeftTreeEntryChild unpacked ->
#             unpacked


def parseInventoryCapacityGaugeText(capacityText: str) -> Union[str, InventoryWindowCapacityGauge]:
    pass
# parseInventoryCapacityGaugeText : str -> Result str InventoryWindowCapacityGauge
# parseInventoryCapacityGaugeText capacityText =
#     let
#         parseMaybeNumber =
#             Maybe.map (str.trim >> parseNumberTruncatingAfterOptionalDecimalSeparator >> Result.map Just)
#                 >> Maybe.withDefault (Ok Nothing)
#         continueWithTexts { usedText, maybeMaximumText, maybeSelectedText } =
#             case usedText |> parseNumberTruncatingAfterOptionalDecimalSeparator of
#                 Err parseNumberError ->
#                     Err ("Failed to parse used number: " ++ parseNumberError)
#                 Ok used ->
#                     case maybeMaximumText |> parseMaybeNumber of
#                         Err parseNumberError ->
#                             Err ("Failed to parse maximum number: " ++ parseNumberError)
#                         Ok maximum ->
#                             case maybeSelectedText |> parseMaybeNumber of
#                                 Err parseNumberError ->
#                                     Err ("Failed to parse selected number: " ++ parseNumberError)
#                                 Ok selected ->
#                                     Ok { used = used, maximum = maximum, selected = selected }
#         continueAfterSeparatingBySlash { beforeSlashText, afterSlashMaybeText } =
#             case beforeSlashText |> str.trim |> str.split ")" of
#                 [ onlyUsedText ] ->
#                     continueWithTexts { usedText = onlyUsedText, maybeMaximumText = afterSlashMaybeText, maybeSelectedText = Nothing }
#                 [ firstPart, secondPart ] ->
#                     continueWithTexts { usedText = secondPart, maybeMaximumText = afterSlashMaybeText, maybeSelectedText = Just (firstPart |> str.replace "(" "") }
#                 _ ->
#                     Err ("Unexpected number of components in text before slash '" ++ beforeSlashText ++ "'")
#     in
#     case capacityText |> str.replace "m³" "" |> str.split "/" of
#         [ withoutSlash ] ->
#             continueAfterSeparatingBySlash { beforeSlashText = withoutSlash, afterSlashMaybeText = Nothing }
#         [ partBeforeSlash, partAfterSlash ] ->
#             continueAfterSeparatingBySlash { beforeSlashText = partBeforeSlash, afterSlashMaybeText = Just partAfterSlash }
#         _ ->
#             Err ("Unexpected number of components in capacityText '" ++ capacityText ++ "'")


def parseModuleButtonTooltipFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[ModuleButtonTooltip]:
    pass
# parseModuleButtonTooltipFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe ModuleButtonTooltip
# parseModuleButtonTooltipFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ModuleButtonTooltip")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just uiNode ->
#             Just (parseModuleButtonTooltip uiNode)


def parseModuleButtonTooltip(tooltipUINode: UITreeNodeWithDisplayRegion) -> ModuleButtonTooltip:
    pass
# parseModuleButtonTooltip : UITreeNodeWithDisplayRegion -> ModuleButtonTooltip
# parseModuleButtonTooltip tooltipUINode =
#     let
#         upperRightCornerFromDisplayRegion region =
#             { x = region.x + region.width, y = region.y }
#         distanceSquared a b =
#             let
#                 distanceX =
#                     a.x - b.x
#                 distanceY =
#                     a.y - b.y
#             in
#             distanceX * distanceX + distanceY * distanceY
#         shortcutCandidates =
#             tooltipUINode
#                 |> getAllContainedDisplayTextsWithRegion
#                 |> List.map
#                     (\( text, textUINode ) ->
#                         { text = text
#                         , distanceUpperRightCornerSquared =
#                             distanceSquared
#                                 (textUINode.totalDisplayRegion |> upperRightCornerFromDisplayRegion)
#                                 (tooltipUINode.totalDisplayRegion |> upperRightCornerFromDisplayRegion)
#                         }
#                     )
#                 |> List.sortBy .distanceUpperRightCornerSquared
#         shortcut =
#             shortcutCandidates
#                 |> List.filter (\textAndDistance -> textAndDistance.distanceUpperRightCornerSquared < 1000)
#                 |> List.head
#                 |> Maybe.map (\{ text } -> { text = text, parseResult = text |> parseModuleButtonTooltipShortcut })
#         optimalRangestr =
#             tooltipUINode.uiNode
#                 |> getAllContainedDisplayTexts
#                 |> List.filterMap
#                     (\text ->
#                         "Optimal range (|within)\\s*([\\d\\.]+\\s*[km]+)"
#                             |> Regex.fromstr
#                             |> Maybe.andThen (\regex -> text |> Regex.find regex |> List.head)
#                             |> Maybe.andThen (.submatches >> List.drop 1 >> List.head)
#                             |> Maybe.andThen identity
#                             |> Maybe.map str.trim
#                     )
#                 |> List.head
#         optimalRange =
#             optimalRangestr
#                 |> Maybe.map (\asstr -> { asstr = asstr, inMeters = asstr |> parseOverviewEntryDistanceInMetersFromText })
#     in
#     { uiNode = tooltipUINode
#     , shortcut = shortcut
#     , optimalRange = optimalRange
#     }


def parseModuleButtonTooltipShortcut(shortcutText: str) -> Union[str, List[CUSTOMKEYCODE]]:
    pass
# parseModuleButtonTooltipShortcut : str -> Result str (List Common.EffectOnWindow.VirtualKeyCode)
# parseModuleButtonTooltipShortcut shortcutText =
#     shortcutText
#         |> str.split "-"
#         |> List.concatMap (str.split "+")
#         |> List.map str.trim
#         |> List.filter (str.length >> (<) 0)
#         |> List.foldl
#             (\nextKeyText previousResult ->
#                 previousResult
#                     |> Result.andThen
#                         (\previousKeys ->
#                             case nextKeyText |> parseKeyShortcutText of
#                                 Just nextKey ->
#                                     Ok (nextKey :: previousKeys)
#                                 Nothing ->
#                                     Err ("Unknown key text: '" ++ nextKeyText ++ "'")
#                         )
#             )
#             (Ok [])
#         |> Result.map List.reverse


def parseKeyShortcutText(keytext: str) -> Optional[CUSTOMKEYCODE]:
    pass
# parseKeyShortcutText : str -> Maybe Common.EffectOnWindow.VirtualKeyCode
# parseKeyShortcutText keyText =
#     [ ( "CTRL", Common.EffectOnWindow.vkey_LCONTROL )
#     , ( "STRG", Common.EffectOnWindow.vkey_LCONTROL )
#     , ( "ALT", Common.EffectOnWindow.vkey_LMENU )
#     , ( "SHIFT", Common.EffectOnWindow.vkey_LSHIFT )
#     , ( "UMSCH", Common.EffectOnWindow.vkey_LSHIFT )
#     , ( "F1", Common.EffectOnWindow.vkey_F1 )
#     , ( "F2", Common.EffectOnWindow.vkey_F2 )
#     , ( "F3", Common.EffectOnWindow.vkey_F3 )
#     , ( "F4", Common.EffectOnWindow.vkey_F4 )
#     , ( "F5", Common.EffectOnWindow.vkey_F5 )
#     , ( "F6", Common.EffectOnWindow.vkey_F6 )
#     , ( "F7", Common.EffectOnWindow.vkey_F7 )
#     , ( "F8", Common.EffectOnWindow.vkey_F8 )
#     , ( "F9", Common.EffectOnWindow.vkey_F9 )
#     , ( "F10", Common.EffectOnWindow.vkey_F10 )
#     , ( "F11", Common.EffectOnWindow.vkey_F11 )
#     , ( "F12", Common.EffectOnWindow.vkey_F12 )
#     ]
#         |> Dict.fromList
#         |> Dict.get (keyText |> str.toUpper)


def parseChatWindowStacksFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> List[ChatWindowStack]:

    matches = (x for x in listDescendantsWithDisplayRegion(uiTreeRoot) if x.uiNode.pythonObjectTypeName == 'ChatWindowStack')
    return [ parseChatWindowStack(x) for x in matches ]
# parseChatWindowStacksFromUITreeRoot : UITreeNodeWithDisplayRegion -> List ChatWindowStack
# parseChatWindowStacksFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ChatWindowStack")
#         |> List.map parseChatWindowStack


def parseChatWindowStack(chatWindowStackUiNode: UITreeNodeWithDisplayRegion) -> ChatWindowStack:
    _s = [y for y in listDescendantsWithDisplayRegion(chatWindowStackUiNode) if y.uiNode.pythonObjectTypeName == 'XmppChatWindow']
    chatWindowNode = _s[0]
    result = ChatWindowStack()
    result.uiNode = chatWindowStackUiNode
    result.chatWindow = parseChatWindow(chatWindowNode)
    return result

# parseChatWindowStack : UITreeNodeWithDisplayRegion -> ChatWindowStack
# parseChatWindowStack chatWindowStackUiNode =
#     let
#         chatWindowNode =
#             chatWindowStackUiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "XmppChatWindow")
#                 |> List.head
#     in
#     { uiNode = chatWindowStackUiNode
#     , chatWindow = chatWindowNode |> Maybe.map parseChatWindow
#     }


def parseChatWindow(chatWindowuiNode: UITreeNodeWithDisplayRegion) -> ChatWindow:
    userListNode: List[UITreeNodeWithDisplayRegion] = []
    keys = {}
    for x in listDescendantsWithDisplayRegion(chatWindowuiNode):
        _r = getNameFromDictEntries(x.uiNode)
        # print(_r)
        keys[x] = _r
        if _r is not None and 'userlist' == _r:
            userListNode.append(x)
    print("------------")
    print(userListNode)
    _firstNode = userListNode[0]
    result = ChatWindow()
    result.uiNode = _firstNode
    result.name = keys[_firstNode]
    print("Name: ", result.name)
    result.userlist = parseChatWindowUserlist(_firstNode)
    return result
# parseChatWindow : UITreeNodeWithDisplayRegion -> ChatWindow
# parseChatWindow chatWindowUiNode =
#     let
#         userlistNode =
#             chatWindowUiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map (str.toLower >> str.contains "userlist") >> Maybe.withDefault False)
#                 |> List.head
#     in
#     { uiNode = chatWindowUiNode
#     , name = getNameFromDictEntries chatWindowUiNode.uiNode
#     , userlist = userlistNode |> Maybe.map parseChatWindowUserlist
#     }


def parseChatWindowUserlist(userListNode: UITreeNodeWithDisplayRegion) -> ChatWindowUserlist:
    # visibleUsers = [x for x in listDescendantsWithDisplayRegion(userListNode) if foldl()]
    visibleUsers = []
    scrollDisplayRegions = []
    for x in listDescendantsWithDisplayRegion(userListNode):
        if x.uiNode.pythonObjectTypeName in ['XmppChatSimpleUserEntry','XmppChatUserEntry']:
            print("Raw: ", x.uiNode.pythonObjectTypeName, x.uiNode.pythonObjectAddress)
            _c = parseChatUserEntry(x)
            print("_c", _c)
            visibleUsers.append(_c)
        if 'ScrollControls' in x.uiNode.pythonObjectTypeName:
            scrollDisplayRegions.append(x)
    scrollControls = parseScrollControls(scrollDisplayRegions[0]) if len(scrollDisplayRegions) > 0 else None
    result = ChatWindowUserlist()
    result.uiNode = userListNode
    result.visibleUsers = visibleUsers
    result.scrollControls = scrollControls
    return result
# parseChatWindowUserlist : UITreeNodeWithDisplayRegion -> ChatWindowUserlist
# parseChatWindowUserlist userlistNode =
#     let
#         visibleUsers =
#             userlistNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (\uiNode -> [ "XmppChatSimpleUserEntry", "XmppChatUserEntry" ] |> List.member uiNode.uiNode.pythonObjectTypeName)
#                 |> List.map parseChatUserEntry
#         scrollControls =
#             userlistNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "ScrollControls")
#                 |> List.head
#                 |> Maybe.map parseScrollControls
#     in
#     { uiNode = userlistNode, visibleUsers = visibleUsers, scrollControls = scrollControls }


def parseChatUserEntry(chatUserUiNode: UITreeNodeWithDisplayRegion) -> ChatUserEntry:
    print("Testing List: ")
    pprint(chatUserUiNode)
    print(vars(chatUserUiNode))
    print([x.uiNode.pythonObjectTypeName for x in listDescendantsWithDisplayRegion(chatUserUiNode)])
    print("Done.")

    standingIconNodes = [x for x in listDescendantsWithDisplayRegion(chatUserUiNode) if x.uiNode.pythonObjectTypeName == 'FlagIconWithState']
    print(standingIconNodes)
    standingIconNode = standingIconNodes[0] if len(standingIconNodes) > 0 else None
    names = [x for x in getAllContainedDisplayTexts(chatUserUiNode.uiNode) if x is not None]
    names.sort( key=len, reverse=True)
    print("Names: " , names)
    name = names[0]
    standingIconHint = None
    if standingIconNode is not None:
        standingIconHint = getHintTextFromDictEntries(standingIconNode.uiNode) 
    result = ChatUserEntry()
    result.name = name
    result.standingIconHint = standingIconHint
    result.uiNode = chatUserUiNode
    return result
    
# parseChatUserEntry : UITreeNodeWithDisplayRegion -> ChatUserEntry
# parseChatUserEntry chatUserUiNode =
#     let
#         standingIconNode =
#             chatUserUiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "FlagIconWithState")
#                 |> List.head
#         name =
#             chatUserUiNode.uiNode
#                 |> getAllContainedDisplayTexts
#                 |> List.sortBy str.length
#                 |> List.reverse
#                 |> List.head
#         standingIconHint =
#             standingIconNode
#                 |> Maybe.andThen (.uiNode >> getHintTextFromDictEntries)
#     in
#     { uiNode = chatUserUiNode
#     , name = name
#     , standingIconHint = standingIconHint
#     }


def parseAgentConversationWindowsFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> List[AgentConversationWindow]:
    pass
# parseAgentConversationWindowsFromUITreeRoot : UITreeNodeWithDisplayRegion -> List AgentConversationWindow
# parseAgentConversationWindowsFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "AgentDialogueWindow")
#         |> List.map parseAgentConversationWindow


def parseAgentConversationWindow(windowUINode: UITreeNodeWithDisplayRegion) -> AgentConversationWindow:
    pass
# parseAgentConversationWindow : UITreeNodeWithDisplayRegion -> AgentConversationWindow
# parseAgentConversationWindow windowUINode =
#     { uiNode = windowUINode
#     }


def parseMarketOrdersWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[MarketOrdersWindow]:
    pass
# parseMarketOrdersWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe MarketOrdersWindow
# parseMarketOrdersWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "MarketOrdersWnd")
#         |> List.head
#         |> Maybe.map parseMarketOrdersWindow


def parseMarketOrdersWindow(windowUINode: UITreeNodeWithDisplayRegion) -> MarketOrdersWindow:
    pass
# parseMarketOrdersWindow : UITreeNodeWithDisplayRegion -> MarketOrdersWindow
# parseMarketOrdersWindow windowUINode =
#     { uiNode = windowUINode
#     }


def parseFittingWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[FittingWindow]:
    pass
# parseFittingWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe FittingWindow
# parseFittingWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "FittingWindow")
#         |> List.head
#         |> Maybe.map parseFittingWindow


def parseFittingWindow(windowUINode: UITreeNodeWithDisplayRegion) -> FittingWindow:
    pass
# parseFittingWindow : UITreeNodeWithDisplayRegion -> FittingWindow
# parseFittingWindow windowUINode =
#     { uiNode = windowUINode
#     }


def parseSurveyScanWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[SurveyScanWindow]:
    pass
# parseSurveyScanWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe SurveyScanWindow
# parseSurveyScanWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SurveyScanView")
#         |> List.head
#         |> Maybe.map parseSurveyScanWindow


def parseSurveyScanWindow(windowUiNode: UITreeNodeWithDisplayRegion) -> SurveyScanWindow:
    pass
# parseSurveyScanWindow : UITreeNodeWithDisplayRegion -> SurveyScanWindow
# parseSurveyScanWindow windowUINode =
#     { uiNode = windowUINode
#     , scanEntries =
#         windowUINode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SurveyScanEntry")
#     }


def parseBookmarkLocationWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[BookmarkLocationWindow]:
    pass
# parseBookmarkLocationWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe BookmarkLocationWindow
# parseBookmarkLocationWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "BookmarkLocationWindow")
#         |> List.head
#         |> Maybe.map parseBookmarkLocationWindow


def parseBookmarkLocationWindow(windowuinode: UITreeNodeWithDisplayRegion) -> BookmarkLocationWindow:
    pass
# parseBookmarkLocationWindow : UITreeNodeWithDisplayRegion -> BookmarkLocationWindow
# parseBookmarkLocationWindow windowUINode =
#     let
#         buttonFromLabelText labelText =
#             windowUINode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "Button")
#                 |> List.filter (.uiNode >> getAllContainedDisplayTexts >> List.map (str.trim >> str.toLower) >> List.member (labelText |> str.toLower))
#                 |> List.sortBy (.totalDisplayRegion >> areaFromDisplayRegion >> Maybe.withDefault 0)
#                 |> List.head
#     in
#     { uiNode = windowUINode
#     , submitButton = buttonFromLabelText "submit"
#     , cancelButton = buttonFromLabelText "cancel"
#     }


def parseRepairShopWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[RepairShopWindow]:
    pass
# parseRepairShopWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe RepairShopWindow
# parseRepairShopWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "RepairShopWindow")
#         |> List.head
#         |> Maybe.map parseRepairShopWindow


def uiTreeRoot(windowUINode: UITreeNodeWithDisplayRegion) -> RepairShopWindow:
    pass
# parseRepairShopWindow : UITreeNodeWithDisplayRegion -> RepairShopWindow
# parseRepairShopWindow windowUINode =
#     let
#         buttonFromLabelText labelText =
#             windowUINode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "Button")
#                 |> List.filter (.uiNode >> getAllContainedDisplayTexts >> List.map (str.trim >> str.toLower) >> List.member (labelText |> str.toLower))
#                 |> List.sortBy (.totalDisplayRegion >> areaFromDisplayRegion >> Maybe.withDefault 0)
#                 |> List.head
#     in
#     { uiNode = windowUINode
#     , items =
#         windowUINode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "Item")
#     , repairItemButton = buttonFromLabelText "repair item"
#     , pickNewItemButton = buttonFromLabelText "pick new item"
#     , repairAllButton = buttonFromLabelText "repair all"
#     }


def parseCharacterSheetWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[CharacterSheetWindow]:
    pass
# parseCharacterSheetWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe CharacterSheetWindow
# parseCharacterSheetWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "CharacterSheetWindow")
#         |> List.head
#         |> Maybe.map parseCharacterSheetWindow


def parseCharacterSheetWindow(windowUINode: UITreeNodeWithDisplayRegion) -> CharacterSheetWindow:
    pass
# parseCharacterSheetWindow : UITreeNodeWithDisplayRegion -> CharacterSheetWindow
# parseCharacterSheetWindow windowUINode =
#     let
#         skillGroups =
#             windowUINode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "SkillGroupGauge")
#     in
#     { uiNode = windowUINode
#     , skillGroups = skillGroups
#     }


def parseFleetWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[FleetWindow]:
    pass
# parseFleetWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe FleetWindow
# parseFleetWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "FleetWindow")
#         |> List.head
#         |> Maybe.map parseFleetWindow


def parseFleetwindow(windowUINode: UITreeNodeWithDisplayRegion) -> FleetWindow:
    pass
# parseFleetWindow : UITreeNodeWithDisplayRegion -> FleetWindow
# parseFleetWindow windowUINode =
#     let
#         fleetMembers =
#             windowUINode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "FleetMember")
#     in
#     { uiNode = windowUINode
#     , fleetMembers = fleetMembers
#     }


def parseWatchListPanelFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[WatchListPanel]:
    pass
# parseWatchListPanelFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe WatchListPanel
# parseWatchListPanelFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "WatchListPanel")
#         |> List.head
#         |> Maybe.map parseWatchListPanel


def parseWatchListPanel(windowUINode: UITreeNodeWithDisplayRegion) -> WatchListPanel:
    pass
# parseWatchListPanel : UITreeNodeWithDisplayRegion -> WatchListPanel
# parseWatchListPanel windowUINode =
#     let
#         entries =
#             windowUINode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "WatchListEntry")
#     in
#     { uiNode = windowUINode
#     , entries = entries
#     }


def parseStandaloneBookmarkWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[StandaloneBookmarkWindow]:
    pass
# parseStandaloneBookmarkWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe StandaloneBookmarkWindow
# parseStandaloneBookmarkWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "StandaloneBookmarkWnd")
#         |> List.head
#         |> Maybe.map parseStandaloneBookmarkWindow


def parseStandaloneBookmarkWindow(windowUINode: UITreeNodeWithDisplayRegion) -> StandaloneBookmarkWindow:
    pass
# parseStandaloneBookmarkWindow : UITreeNodeWithDisplayRegion -> StandaloneBookmarkWindow
# parseStandaloneBookmarkWindow windowUINode =
#     let
#         entries =
#             windowUINode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "PlaceEntry")
#     in
#     { uiNode = windowUINode
#     , entries = entries
#     }


def parseNeocomFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[Neocom]:
    pass
# parseNeocomFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe Neocom
# parseNeocomFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "Neocom")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just uiNode ->
#             Just (parseNeocom uiNode)


def parseNeocom(neocomUiNode: UITreeNodeWithDisplayRegion) -> Neocom:
    pass
# parseNeocom : UITreeNodeWithDisplayRegion -> Neocom
# parseNeocom neocomUiNode =
#     let
#         maybeClockTextAndNode =
#             neocomUiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "InGameClock")
#                 |> List.concatMap getAllContainedDisplayTextsWithRegion
#                 |> List.head
#         nodeFromTexturePathEnd texturePathEnd =
#             neocomUiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter
#                     (.uiNode
#                         >> getTexturePathFromDictEntries
#                         >> Maybe.map (str.endsWith texturePathEnd)
#                         >> Maybe.withDefault False
#                     )
#                 |> List.head
#         clock =
#             maybeClockTextAndNode
#                 |> Maybe.map
#                     (\( clockText, clockNode ) ->
#                         { uiNode = clockNode
#                         , text = clockText
#                         , parsedText = parseNeocomClockText clockText
#                         }
#                     )
#     in
#     { uiNode = neocomUiNode
#     , iconInventory = nodeFromTexturePathEnd "items.png"
#     , clock = clock
#     }


def parseNeocomClockText(clockText: str) -> Union[str, ParsedTime]:
    pass
# parseNeocomClockText : str -> Result str { hour : int, minute : int }
# parseNeocomClockText clockText =
#     case clockText |> str.split ":" of
#         [ hourText, minuteText ] ->
#             case hourText |> str.trim |> str.toint of
#                 Nothing ->
#                     Err ("Failed to parse hour: '" ++ hourText ++ "'")
#                 Just hour ->
#                     case minuteText |> str.trim |> str.toint of
#                         Nothing ->
#                             Err ("Failed to parse minute: '" ++ minuteText ++ "'")
#                         Just minute ->
#                             Ok { hour = hour, minute = minute }
#         _ ->
#             Err "Expecting exactly two substrs separated by a colon (:)."


def parseKeyActivationWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[KeyActivationWindow]:
    pass
# parseKeyActivationWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe KeyActivationWindow
# parseKeyActivationWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "KeyActivationWindow")
#         |> List.head
#         |> Maybe.map parseKeyActivationWindow


def parseKeyActiationWindow(windowUiNode: UITreeNodeWithDisplayRegion) -> KeyActivationWindow:
    pass
# parseKeyActivationWindow : UITreeNodeWithDisplayRegion -> KeyActivationWindow
# parseKeyActivationWindow windowUiNode =
#     let
#         activateButton =
#             windowUiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ActivateButton")
#                 |> List.head
#     in
#     { uiNode = windowUiNode
#     , activateButton = activateButton
#     }


def parseExpander(uiNode: UITreeNodeWithDisplayRegion) -> Expander:
    pass
# parseExpander : UITreeNodeWithDisplayRegion -> Expander
# parseExpander uiNode =
#     let
#         maybeTexturePath =
#             getTexturePathFromDictEntries uiNode.uiNode
#         isExpanded =
#             maybeTexturePath
#                 |> Maybe.andThen
#                     (\texturePath ->
#                         [ ( "38_16_228.png", False ), ( "38_16_229.png", True ) ]
#                             |> List.filter (\( pathEnd, _ ) -> texturePath |> str.endsWith pathEnd)
#                             |> List.map Tuple.second
#                             |> List.head
#                     )
#     in
#     { uiNode = uiNode
#     , texturePath = maybeTexturePath
#     , isExpanded = isExpanded
#     }


def parseMessageBoxesFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> List[MessageBox]:
    pass
# parseMessageBoxesFromUITreeRoot : UITreeNodeWithDisplayRegion -> List MessageBox
# parseMessageBoxesFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "MessageBox")
#         |> List.map parseMessageBox


def parseMessageBox(uiNode: UITreeNodeWithDisplayRegion) -> MessageBox:
    pass
# parseMessageBox : UITreeNodeWithDisplayRegion -> MessageBox
# parseMessageBox uiNode =
#     let
#         buttons =
#             uiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "Button")
#                 |> List.map
#                     (\buttonNode ->
#                         { uiNode = buttonNode
#                         , maintext =
#                             buttonNode
#                                 |> getAllContainedDisplayTextsWithRegion
#                                 |> List.sortBy (Tuple.second >> .totalDisplayRegion >> areaFromDisplayRegion >> Maybe.withDefault 0)
#                                 |> List.map Tuple.first
#                                 |> List.head
#                         }
#                     )
#     in
#     { buttons = buttons
#     , uiNode = uiNode
#     }


def parseScrollControls(scrollControlsNode: UITreeNodeWithDisplayRegion) -> ScrollControls:
    scrollHandles = [x for x in listDescendantsWithDisplayRegion(scrollControlsNode) if x.uiNode.pythonObjectTypeName == 'ScrollHandle' ]
    scrollHandle = scrollHandles[0]
    sc = ScrollControls()
    sc.scrollHandle = scrollHandle
    sc.uiNode = scrollControlsNode
    return sc
# parseScrollControls : UITreeNodeWithDisplayRegion -> ScrollControls
# parseScrollControls scrollControlsNode =
#     let
#         scrollHandle =
#             scrollControlsNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ScrollHandle")
#                 |> List.head
#     in
#     { uiNode = scrollControlsNode
#     , scrollHandle = scrollHandle
#     }


def parseLayerAbovemainFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[UITreeNodeWithDisplayRegion]:
    pass
# parseLayerAbovemainFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe UITreeNodeWithDisplayRegion
# parseLayerAbovemainFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> getNameFromDictEntries >> (==) (Just "l_abovemain"))
#         |> List.head


def getSubstrBetweenXmlTagsAfterMarker(marker: str) -> Callable[[str], Optional[str]]:
    def fn(x: str) -> Optional[str]:
        pass
    return fn
# getSubstrBetweenXmlTagsAfterMarker : str -> str -> Maybe str
# getSubstrBetweenXmlTagsAfterMarker marker =
#     str.split marker
#         >> List.drop 1
#         >> List.head
#         >> Maybe.andThen (str.split ">" >> List.drop 1 >> List.head)
#         >> Maybe.andThen (str.split "<" >> List.head)


def parseNumberTruncatingAfterOptionalDecimalSeparator(numberDisplayText: str) -> Union[str, int]:
    pass
# parseNumberTruncatingAfterOptionalDecimalSeparator : str -> Result str int
# parseNumberTruncatingAfterOptionalDecimalSeparator numberDisplayText =
#     let
#         expectedSeparators =
#             [ ",", ".", "’", " ", "\u{00A0}", "\u{202F}" ]
#         groupsTexts =
#             expectedSeparators
#                 |> List.foldl (\separator -> List.concatMap (str.split separator))
#                     [ str.trim numberDisplayText ]
#         lastGroupIsFraction =
#             case List.reverse groupsTexts of
#                 lastGroupText :: _ :: _ ->
#                     str.length lastGroupText < 3
#                 _ ->
#                     False
#         integerText =
#             str.join ""
#                 (if lastGroupIsFraction then
#                     groupsTexts |> List.reverse |> List.drop 1 |> List.reverse
#                  else
#                     groupsTexts
#                 )
#     in
#     integerText
#         |> str.toint
#         |> Result.fromMaybe ("Failed to parse to integer: " ++ integerText)


def centerFromDisplayRegion(region: DisplayRegion) -> Location2d:
    pass
# centerFromDisplayRegion : DisplayRegion -> Location2d
# centerFromDisplayRegion region =
#     { x = region.x + region.width // 2, y = region.y + region.height // 2 }


def getDisplayText(uiNode: UITreeNode) -> Optional[str]:
    _s = ('_setText', '_text')
    for s in _s:
        _n = uiNode.dictEntriesOfInterest.get(s, None)
        if _n is not None:
            return _n
    return None
# getDisplayText : UITreeNode -> Maybe str
# getDisplayText uiNode =
#     [ "_setText", "_text" ]
#         |> List.filterMap
#             (\displayTextPropertyName ->
#                 uiNode.dictEntriesOfinterest
#                     |> Dict.get displayTextPropertyName
#                     |> Maybe.andThen (Json.Decode.decodeValue Json.Decode.str >> Result.toMaybe)
#             )
#         |> List.sortBy (str.length >> negate)
#         |> List.head

def getAllContainedDisplayTexts(uiNode: UITreeNode) -> List[str]:
    _list = [uiNode]
    _decendants = listDescendantsInUITreeNode(uiNode)
    if _decendants is not None:
        _list.extend(_decendants)
    return [getDisplayText(x) for x in _list if x is not None ]
# getAllContainedDisplayTexts : UITreeNode -> List str
# getAllContainedDisplayTexts uiNode =
#     uiNode
#         :: (uiNode |> listDescendantsInUITreeNode)
#         |> List.filterMap getDisplayText

# getAllContainedDisplayTextsWithRegion : UITreeNodeWithDisplayRegion -> List ( str, UITreeNodeWithDisplayRegion )
# getAllContainedDisplayTextsWithRegion uiNode =
#     uiNode
#         :: (uiNode |> listDescendantsWithDisplayRegion)
#         |> List.filterMap
#             (\descendant ->
#                 let
#                     displayText =
#                         descendant.uiNode |> getDisplayText |> Maybe.withDefault ""
#                 in
#                 if 0 < (displayText |> str.length) then
#                     Just ( displayText, descendant )
#                 else
#                     Nothing
#             )


def getNameFromDictEntries(x: UITreeNode) -> Optional[str]:
    return x.dictEntriesOfInterest.get("_name")
# getNameFromDictEntries : UITreeNode -> Maybe str
# getNameFromDictEntries =
#     getstrPropertyFromDictEntries "_name"


def getHintTextFromDictEntries(x: UITreeNode) -> Optional[str]:
    return x.dictEntriesOfInterest.get("_hint")
# getHintTextFromDictEntries : UITreeNode -> Maybe str
# getHintTextFromDictEntries =
#     getstrPropertyFromDictEntries "_hint"


def getTexturePathFromDictEntries(x: UITreeNode) -> Optional[str]:
    return x.dictEntriesOfInterest.get('texturePath')
# getTexturePathFromDictEntries : UITreeNode -> Maybe str
# getTexturePathFromDictEntries =
#     getstrPropertyFromDictEntries "texturePath"


# def getstrPropertyFromDictEntries(dictEntryKey: str) -> Callable[[UITreeNode], Optional[str]]:
#     def fn(x: UITreeNode) -> Optional[str]:
#         pass
#     return fn
# getstrPropertyFromDictEntries : str -> UITreeNode -> Maybe str
# getstrPropertyFromDictEntries dictEntryKey uiNode =
#     uiNode.dictEntriesOfinterest
#         |> Dict.get dictEntryKey
#         |> Maybe.andThen (Json.Decode.decodeValue Json.Decode.str >> Result.toMaybe)


def getColorPercentFromDictEntries(x: UITreeNode) -> Optional[ColorComponents]:
    pass
# getColorPercentFromDictEntries : UITreeNode -> Maybe ColorComponents
# getColorPercentFromDictEntries =
#     .dictEntriesOfinterest
#         >> Dict.get "_color"
#         >> Maybe.andThen (Json.Decode.decodeValue jsonDecodeColorPercent >> Result.toMaybe)


def jsonDecodeColorPercent(x):
    pass
# jsonDecodeColorPercent : Json.Decode.Decoder ColorComponents
# jsonDecodeColorPercent =
#     Json.Decode.map4 ColorComponents
#         (Json.Decode.field "aPercent" jsonDecodeintFromintOrstr)
#         (Json.Decode.field "rPercent" jsonDecodeintFromintOrstr)
#         (Json.Decode.field "gPercent" jsonDecodeintFromintOrstr)
#         (Json.Decode.field "bPercent" jsonDecodeintFromintOrstr)


def getRotationFloatFromDictEntries(x: UITreeNode) -> Optional[float]:
    pass
# getRotationFloatFromDictEntries : UITreeNode -> Maybe Float
# getRotationFloatFromDictEntries =
#     .dictEntriesOfinterest
#         >> Dict.get "_rotation"
#         >> Maybe.andThen (Json.Decode.decodeValue Json.Decode.float >> Result.toMaybe)


def jsonDecodeintFromintOrstr(x):
    pass
# jsonDecodeintFromintOrstr : Json.Decode.Decoder int
# jsonDecodeintFromintOrstr =
#     Json.Decode.oneOf
#         [ Json.Decode.int
#         , Json.Decode.str
#             |> Json.Decode.andThen
#                 (\asstr ->
#                     case asstr |> str.toint of
#                         Just asint ->
#                             Json.Decode.succeed asint
#                         Nothing ->
#                             Json.Decode.fail ("Failed to parse integer from str '" ++ asstr ++ "'")
#                 )
#         ]


def getHorizontalOffsetFromParentAndWidth(uiNode: UITreeNode) -> Optional[OffsetWidth]:
    pass
# getHorizontalOffsetFromParentAndWidth : UITreeNode -> Maybe { offset : int, width : int }
# getHorizontalOffsetFromParentAndWidth uiNode =
#     let
#         roundedNumberFromPropertyName propertyName =
#             uiNode.dictEntriesOfinterest
#                 |> Dict.get propertyName
#                 |> Maybe.andThen (Json.Decode.decodeValue Json.Decode.float >> Result.toMaybe)
#                 |> Maybe.map round
#     in
#     case ( roundedNumberFromPropertyName "_displayX", roundedNumberFromPropertyName "_width" ) of
#         ( Just offset, Just width ) ->
#             Just { offset = offset, width = width }
#         _ ->
#             Nothing


def areaFromDisplayRegion(region: DisplayRegion) -> Optional[int]:
    pass
# areaFromDisplayRegion : DisplayRegion -> Maybe int
# areaFromDisplayRegion region =
#     if region.width < 0 || region.height < 0 then
#         Nothing
#     else
#         Just (region.width * region.height)


def getVerticalOffsetFromParent(x: UITreeNode) -> Optional[int]:
    pass
# getVerticalOffsetFromParent : UITreeNode -> Maybe int
# getVerticalOffsetFromParent =
#     .dictEntriesOfinterest
#         >> Dict.get "_displayY"
#         >> Maybe.andThen (Json.Decode.decodeValue Json.Decode.float >> Result.toMaybe)
#         >> Maybe.map round


def getMostPopulousDescendantMatchingPredicate(predicate: Callable[[UITreeNode], bool]) -> Callable:
    def fnA(x) -> Callable[[], Optional[UITreeNode]]:
        def fnB() -> Optional[UITreeNode]:
            pass
        return fnB(x)
    return fnA
# getMostPopulousDescendantMatchingPredicate : (UITreeNode -> bool) -> UITreeNode -> Maybe UITreeNode
# getMostPopulousDescendantMatchingPredicate predicate parent =
#     listDescendantsInUITreeNode parent
#         |> List.filter predicate
#         |> List.sortBy countDescendantsInUITreeNode
#         |> List.reverse
#         |> List.head

def listDescendantsInUITreeNode(parent: UITreeNode) -> List[UITreeNode]:
    _p = parent.children or []
    _r = [unwrapUITreeNodeChild(x) for x in _p]
    result: List[UITreeNode] = []
    for x in _r:
        result.append(x)
        result.extend(listDescendantsInUITreeNode(x))
    return result

# listDescendantsInUITreeNode : UITreeNode -> List UITreeNode
# listDescendantsInUITreeNode parent =
#     parent.children
#         |> Maybe.withDefault []
#         |> List.map unwrapUITreeNodeChild
#         |> List.concatMap (\child -> child :: listDescendantsInUITreeNode child)



def listDescendantsWithDisplayRegion(parent: UITreeNodeWithDisplayRegion) -> List[UITreeNodeWithDisplayRegion]:
    result = []
    print("listDecesnatsWithDisplayRegion")
    pprint(parent)

    for child in listChildrenWithDisplayRegion(parent):
        print("Child Address: ", child.uiNode.pythonObjectAddress)
        result.append(child)
        result.extend(listDescendantsWithDisplayRegion(child))
    print("ListDescendantsWithDisplayRegion :", result)
    return result

# listDescendantsWithDisplayRegion : UITreeNodeWithDisplayRegion -> List UITreeNodeWithDisplayRegion
# listDescendantsWithDisplayRegion parent =
#     parent
#         |> listChildrenWithDisplayRegion
#         |> List.concatMap (\child -> child :: listDescendantsWithDisplayRegion child)


def listChildrenWithDisplayRegion(parent: UITreeNodeWithDisplayRegion) -> List[UITreeNodeWithDisplayRegion]:
    print("Child Nodes: ", parent.children)
    d = parent.children or []
    print("D: ", [type(child) for child in d])
    
    return [ child for child in d if type(child) == UITreeNodeWithDisplayRegion]
            
# listChildrenWithDisplayRegion : UITreeNodeWithDisplayRegion -> List UITreeNodeWithDisplayRegion
# listChildrenWithDisplayRegion parent =
#     parent.children
#         |> Maybe.withDefault []
#         |> List.filterMap
#             (\child ->
#                 case child of
#                     ChildWithoutRegion _ ->
#                         Nothing
#                     ChildWithRegion childWithRegion ->
#                         Just childWithRegion
#             )
