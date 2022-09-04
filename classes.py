
from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional, Set, Union


# Not Sure what this means at the common. Will need to check into it.
#  Wraping in a Try-Except in order to catch until I determine what it is.
try:
    CUSTOMKEYCODE = Common.EffectOnWindow.VirtualKeyCode
except:
    CUSTOMKEYCODE = None


class UITreeNode:
    pass


class DisplayRegion:
    x: int
    y: int
    width: int
    height: int


class ChildOfNodeWithDisplayRegion(Enum):
    ChildWithRegion = None  # UITreeNodeWithDisplayRegion
    ChildWithoutRegion = UITreeNode


class UITreeNodeWithDisplayRegion:
    uiNode: UITreeNode
    children: Optional[List[ChildOfNodeWithDisplayRegion]]
    selfDisplayRegion: DisplayRegion
    totalDisplayRegion: DisplayRegion


class Location2d:
    x: int
    y: int


class ColorComponents:
    a: int
    r: int
    g: int
    b: int


class ContextMenuEntry:
    uiNode: UITreeNodeWithDisplayRegion
    text: str


class ContextMenu:
    uiNode: UITreeNodeWithDisplayRegion
    entries: List[ContextMenuEntry]


class ShipUIModuleButton:
    uiNode: UITreeNodeWithDisplayRegion
    slotUINode: UITreeNodeWithDisplayRegion
    isActive: Optional[bool]
    isHiliteVisible: bool
    rampRotationMilli: Optional[int]


class ModuleRows(NamedTuple):
    top: List[ShipUIModuleButton]
    middle: List[ShipUIModuleButton]
    bottom: List[ShipUIModuleButton]


class Hitpoints:
    structure: int
    armor: int
    shield: int


class SquadronAbilityIcon:
    uiNode: UITreeNodeWithDisplayRegion
    quantity: Optional[int]
    ramp_active: Optional[bool]


class SquadronUI:
    uiNode: UITreeNodeWithDisplayRegion
    abilities: List[SquadronAbilityIcon]
    actionLabel: Optional[UITreeNodeWithDisplayRegion]


class SquadronsUI:
    uiNode: UITreeNodeWithDisplayRegion
    squadrons: List[SquadronUI]


class ShipUICapacitorPmark:
    uiNode: UITreeNodeWithDisplayRegion
    colorPercent: Optional[ColorComponents]


class ShipUICapacitor:
    uiNode: UITreeNodeWithDisplayRegion
    pmarks: List[ShipUICapacitorPmark]
    levelFromPmarksPercent: Optional[int]


class ShipManeuverType(Enum):
    ManeuverWarp = 0,
    ManeuverJump = 1,
    ManeuverOrbit = 2,
    ManeuverApproach = 3


class ShipUIIndication:
    uiNode: UITreeNodeWithDisplayRegion
    maneuverType: Optional[ShipManeuverType]


class ShipUI:
    uiNode: UITreeNodeWithDisplayRegion
    capacitor: ShipUICapacitor
    hitpointsPercent: Hitpoints
    indication: Optional[ShipUIIndication]
    moduleButtons: List[ShipUIModuleButton]
    moduleButtonsRows: ModuleRows

    offensiveBuffButtonNames: List[str]
    squadronsUI: Optional[SquadronsUI]
    stopButton: Optional[UITreeNodeWithDisplayRegion]
    maxSpeedButton: Optional[UITreeNodeWithDisplayRegion]


class InfoPanelIcons:
    uiNode: UITreeNodeWithDisplayRegion
    search: Optional[UITreeNodeWithDisplayRegion]
    locationInfo: Optional[UITreeNodeWithDisplayRegion]
    route: Optional[UITreeNodeWithDisplayRegion]
    agentMissions: Optional[UITreeNodeWithDisplayRegion]
    dailyChallenge: Optional[UITreeNodeWithDisplayRegion]


class InfoPanelRouteRouteElementMarker:
    uiNode: UITreeNodeWithDisplayRegion


class InfoPanelRoute:
    uiNode: UITreeNodeWithDisplayRegion
    routeElementMarker: List[InfoPanelRouteRouteElementMarker]


class InfoPanelLocationInfoExpandedContent:
    currentStationName: Optional[str]


class InfoPanelLocationInfo:
    uiNode: UITreeNodeWithDisplayRegion
    listSurroundingsButton: UITreeNodeWithDisplayRegion
    currentSolarSystemName: Optional[str]
    securityStatusPercent: Optional[int]
    expandedContent: Optional[InfoPanelLocationInfoExpandedContent]


class InfoPanelAgentMissionsEntry:
    uiNode: UITreeNodeWithDisplayRegion


class InfoPanelAgentMissions:
    uiNode: UITreeNodeWithDisplayRegion
    entries: List[InfoPanelAgentMissionsEntry]


class InfoPanelContainer:
    uiNode: UITreeNodeWithDisplayRegion
    icons: Optional[InfoPanelIcons]
    infoPanelLocationInfo: Optional[InfoPanelLocationInfo]
    infoPanelRoute: Optional[InfoPanelRoute]
    infoPanelAgentMissions: Optional[InfoPanelAgentMissions]


class Target:
    uiNode: UITreeNodeWithDisplayRegion
    barAndImageCont: Optional[UITreeNodeWithDisplayRegion]
    textsTopToBottom: List[str]
    isActiveTarget: bool
    assignedContainerNode: Optional[UITreeNodeWithDisplayRegion]
    assignedIcons: List[UITreeNodeWithDisplayRegion]


class OverviewWindowEntryCommonIndications:
    targeting: bool
    targetedByMe: bool
    isJammingMe: bool
    isWarpDisruptingMe: bool


class OverviewWindowEntry:
    uiNode: UITreeNodeWithDisplayRegion
    textsLeftToRight: List[str]
    cellsTexts: Dict[str, str]
    objectDistance: Optional[str]
    objectDistanceInMeters: Union[str, int]
    objectName: Optional[str]
    objectType: Optional[str]
    objectAlliance: Optional[str]
    iconSpriteColorPercent: Optional[ColorComponents]
    namesUnderSpaceObjectIcon: Set[str]
    bgColorFillsPercent: List[ColorComponents]
    rightAlignedIconsHints: List[str]
    commonIndications: OverviewWindowEntryCommonIndications


class ScrollControls:
    uiNode: UITreeNodeWithDisplayRegion
    scrollHandle: Optional[UITreeNodeWithDisplayRegion]


class OverviewWindow:
    uiNode: UITreeNodeWithDisplayRegion
    entriesHeaders: List[Union[str, UITreeNodeWithDisplayRegion]]
    entries: List[OverviewWindowEntry]
    scrollControls: Optional[ScrollControls]


class SelectedItemWindow:
    uiNode: UITreeNodeWithDisplayRegion
    orbitButton: Optional[UITreeNodeWithDisplayRegion]


class FittingWindow:
    uiNode: UITreeNodeWithDisplayRegion


class MarketOrdersWindow:
    uiNode: UITreeNodeWithDisplayRegion


class SurveyScanWindow:
    uiNode: UITreeNodeWithDisplayRegion
    scanEntries: List[UITreeNodeWithDisplayRegion]


class RepairShopWindow:
    uiNode: UITreeNodeWithDisplayRegion
    items: List[UITreeNodeWithDisplayRegion]
    repairItemButton: Optional[UITreeNodeWithDisplayRegion]
    pickNewItemButton: Optional[UITreeNodeWithDisplayRegion]
    repairAllButton: Optional[UITreeNodeWithDisplayRegion]


class CharacterSheetWindow:
    uiNode: UITreeNodeWithDisplayRegion
    skillGroups: List[UITreeNodeWithDisplayRegion]


class Expander:
    uiNode: UITreeNodeWithDisplayRegion
    texturePath: Optional[str]
    isExpanded: Optional[bool]


class DronesWindowDroneGroupHeader:
    uiNode: UITreeNodeWithDisplayRegion
    maintext: Optional[str]
    expander: Expander
    quantityFromTitle: Optional[int]


class DronesWindowEntryGroupStructure:
    header: DronesWindowDroneGroupHeader
    children: List[Any]  # DronesWindowEntry


class DronesWindowEntryDroneStructure:
    uiNode: UITreeNodeWithDisplayRegion
    maintext: Optional[str]
    hitpointsPercent: Optional[Hitpoints]


class DronesWindowEntry(Enum):
    DronesWindowEntryGroup = DronesWindowEntryGroupStructure
    DronesWindowEntryDrone = DronesWindowEntryDroneStructure


class DronesWindow:
    uiNode: UITreeNodeWithDisplayRegion
    droneGroups: List[DronesWindowEntryGroupStructure]
    droneGroupInBay: Optional[DronesWindowEntryGroupStructure]
    droneGroupInLocalSpace: Optional[DronesWindowEntryGroupStructure]


class ProbeScanResult:
    uiNode: UITreeNodeWithDisplayRegion
    textsLeftToRight: List[str]
    cellsTexts: Dict[str, str]
    warpButton: Optional[UITreeNodeWithDisplayRegion]


class ProbeScannerWindow:
    uiNode: UITreeNodeWithDisplayRegion
    scanResults: List[ProbeScanResult]


class DirectionalScannerWindow:
    uiNode: UITreeNodeWithDisplayRegion
    scrollNode: Optional[UITreeNodeWithDisplayRegion]
    scanResults: List[UITreeNodeWithDisplayRegion]


class StationWindow:
    uiNode: UITreeNodeWithDisplayRegion
    undockButton: Optional[UITreeNodeWithDisplayRegion]
    abortUndockButton: Optional[UITreeNodeWithDisplayRegion]


class InventoryWindowLeftTreeEntryChild:
    InventoryWindowLeftTreeEntryChild: Any  # InventoryWindowLeftTreeEntry


class InventoryWindowLeftTreeEntry:
    uiNode: UITreeNodeWithDisplayRegion
    toggleBtn: Optional[UITreeNodeWithDisplayRegion]
    selectRegion: Optional[UITreeNodeWithDisplayRegion]
    text: str
    children: List[InventoryWindowLeftTreeEntryChild]


class InventoryWindowCapacityGauge:
    used: int
    maximum: Optional[int]
    selected: Optional[int]


class Items:
    items: List[UITreeNodeWithDisplayRegion]


class InventoryItemsView(Enum):
    InventoryItemsListView = Items
    InventoryItemsNotListView = Items


class Inventory:
    uiNode: UITreeNodeWithDisplayRegion
    itemsView: Optional[InventoryItemsView]
    scrollControls: Optional[ScrollControls]


class InventoryWindow:
    uiNode: UITreeNodeWithDisplayRegion
    leftTreeEntries: List[InventoryWindowLeftTreeEntry]
    subCaptionLabelText: Optional[str]
    selectedContainerCapacityGauge: Optional[Union[str,
                                                   InventoryWindowCapacityGauge]]
    selectedContainerInventory: Optional[Inventory]
    buttonToSwitchToListView: Optional[UITreeNodeWithDisplayRegion]


class ChatUserEntry:
    uiNode: UITreeNodeWithDisplayRegion
    name: Optional[str]
    standingIconHint: Optional[str]


class ShortCut(NamedTuple):
    text: str
    parseResult: Optional[Union[str, List[CUSTOMKEYCODE]]]


class ChatWindowUserlist:
    uiNode: UITreeNodeWithDisplayRegion
    visibleUsers: List[ChatUserEntry]
    scrollControls: Optional[ScrollControls]


class ChatWindow:
    uiNode: UITreeNodeWithDisplayRegion
    name: Optional[str]
    user: Optional[ChatWindowUserlist]


class ChatWindowStack:
    uiNode: UITreeNodeWithDisplayRegion
    chatWindow: Optional[ChatWindow]


class OptimalRange(NamedTuple):
    asString: str
    inMeteres: Union[str, int]


class ModuleButtonTooltip:
    uiNode: UITreeNodeWithDisplayRegion
    shortcut: Optional[ShortCut]
    optimalRange: Optional[OptimalRange]


class ParsedText(NamedTuple):
    hour: int
    minute: int


class NeocomClock:
    uiNode: UITreeNodeWithDisplayRegion
    text: str
    parsedText: Union[str, ParsedText]


class Neocom:
    uiNode: UITreeNodeWithDisplayRegion
    iconInventory: Optional[UITreeNodeWithDisplayRegion]
    clock: Optional[NeocomClock]


class AgentConversationWindow:
    uiNode: UITreeNodeWithDisplayRegion


class BookmarkLocationWindow:
    uiNode: UITreeNodeWithDisplayRegion
    submitButton: Optional[UITreeNodeWithDisplayRegion]
    cancelButton: Optional[UITreeNodeWithDisplayRegion]


class ButtonTuples(NamedTuple):
    uiNode: UITreeNodeWithDisplayRegion
    maintext: Optional[str]


class MessageBox:
    uiNode: UITreeNodeWithDisplayRegion
    buttons: List[ButtonTuples]


class FleetWindow:
    uiNode: UITreeNodeWithDisplayRegion
    fleetMembers: List[UITreeNodeWithDisplayRegion]


class WatchListPanel:
    uiNode: UITreeNodeWithDisplayRegion
    entries: List[UITreeNodeWithDisplayRegion]


class StandaloneBookmarkWindow:
    uiNode: UITreeNodeWithDisplayRegion
    entries: List[UITreeNodeWithDisplayRegion]


class KeyActivationWindow:
    uiNode: UITreeNodeWithDisplayRegion
    activateButton: Optional[UITreeNodeWithDisplayRegion]


class ParsedUserinterface:
    uiTree: UITreeNodeWithDisplayRegion
    contextMenus: List[ContextMenu]
    shipUI: Optional[ShipUI]
    targets: List[Target]
    infoPanelContainer: Optional[InfoPanelContainer]
    overviewWindow: Optional[OverviewWindow]
    selectedItemWindow: Optional[SelectedItemWindow]
    dronesWindow: Optional[DronesWindow]
    fittingWindow: Optional[FittingWindow]
    probeScannerWindow: Optional[ProbeScannerWindow]
    directionalScannerWindow: Optional[DirectionalScannerWindow]
    stationWindow: Optional[StationWindow]
    inventoryWindows: List[InventoryWindow]
    chatWindowStacks: List[ChatWindowStack]
    agentConversationWindows: List[AgentConversationWindow]
    marketOrdersWindow: Optional[MarketOrdersWindow]
    surveyScanWindow: Optional[SurveyScanWindow]
    bookmarkLocationWindow: Optional[BookmarkLocationWindow]
    repairShopWindow: Optional[RepairShopWindow]
    characterSheetWindow: Optional[CharacterSheetWindow]
    fleetWindow: Optional[FleetWindow]
    watchListPanel: Optional[WatchListPanel]
    standaloneBookmarkWindow: Optional[StandaloneBookmarkWindow]
    moduleButtonTooltip: Optional[ModuleButtonTooltip]
    neocom: Optional[Neocom]
    messageBoxes: List[MessageBox]
    layerAbovemain: Optional[UITreeNodeWithDisplayRegion]
    keyActivationWindow: Optional[KeyActivationWindow]

