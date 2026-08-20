from fastapi import APIRouter
from typing import List
from datetime import datetime
from api.schemas.disaster import AlertBroadcastRequest, AlertBroadcastResponse

router = APIRouter()

ACTIVE_BROADCAST_ALERTS: List[AlertBroadcastResponse] = [
    AlertBroadcastResponse(
        alert_id="alt-001",
        title="EVACUATION WARNING: Vishwamitri River Overflow",
        body="River water level has breached danger mark 2.6m. Sayajigunj & Sector 3 residents must evacuate immediately to Akota Stadium Shelter.",
        severity="CRITICAL",
        disaster_type="FLOOD",
        target_region="Vadodara",
        issued_by="District Disaster Management Authority (DDMA)",
        issued_at="10 mins ago",
        action_required="EVACUATE_IMMEDIATELY",
        affected_population_estimate=48000,
        acknowledgment_required=True
    ),
    AlertBroadcastResponse(
        alert_id="alt-002",
        title="FLASH FLOOD WATCH: Badrinath Highway Route",
        body="Heavy precipitation (>120mm/hr) detected. High risk of debris flow near Joshimath bypass.",
        severity="HIGH",
        disaster_type="LANDSLIDE",
        target_region="Uttarakhand",
        issued_by="State Emergency Operation Center (SEOC)",
        issued_at="35 mins ago",
        action_required="SEEK_HIGH_GROUND",
        affected_population_estimate=12500,
        acknowledgment_required=False
    )
]

@router.post("/alerts/broadcast", response_model=AlertBroadcastResponse)
def broadcast_emergency_alert(request: AlertBroadcastRequest):
    new_alert = AlertBroadcastResponse(
        alert_id=f"alt-{int(datetime.now().timestamp())}",
        title=request.title,
        body=request.body,
        severity=request.severity,
        disaster_type=request.disaster_type,
        target_region=request.target_region,
        issued_by="Authority Command & Control Center (SURAKSHA AI)",
        issued_at="Just now",
        action_required=request.action_required,
        affected_population_estimate=42500,
        acknowledgment_required=(request.severity == "CRITICAL")
    )
    ACTIVE_BROADCAST_ALERTS.insert(0, new_alert)
    return new_alert

@router.get("/alerts/active", response_model=List[AlertBroadcastResponse])
def get_active_emergency_alerts():
    return ACTIVE_BROADCAST_ALERTS
