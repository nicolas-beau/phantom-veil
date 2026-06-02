"""Policy engine for automated threat response."""
import re
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger("phantom-veil.policy")

class Action(Enum):
    ALLOW = "allow"
    LOG = "log"
    QUARANTINE = "quarantine"
    ISOLATE = "isolate"
    ALERT = "alert"
    KILL = "kill"

@dataclass
class PolicyRule:
    name: str
    description: str
    event_type: str
    conditions: Dict[str, Any]
    actions: List[Action]
    priority: int = 0
    enabled: bool = True

@dataclass
class PolicyDecision:
    rule_name: str
    action: Action
    reason: str
    event_details: dict

class PolicyEngine:
    """Evaluate threat events against security policies."""

    def __init__(self):
        self.rules: List[PolicyRule] = []
        self.decision_log: List[PolicyDecision] = []
        self._load_default_rules()

    def _load_default_rules(self):
        """Load default security policies."""
        self.rules = [
            PolicyRule(
                name="critical-injection",
                description="Auto-quarantine on critical process injection",
                event_type="process_injection",
                conditions={"confidence": ">=", "value": 0.85},
                actions=[Action.QUARANTINE, Action.ALERT],
                priority=100,
            ),
            PolicyRule(
                name="lateral-movement-block",
                description="Block lateral movement attempts",
                event_type="lateral_movement",
                conditions={"confidence": ">=", "value": 0.80},
                actions=[Action.ISOLATE, Action.ALERT],
                priority=90,
            ),
            PolicyRule(
                name="fileless-malware-kill",
                description="Kill and snapshot fileless malware",
                event_type="fileless_malware",
                conditions={"confidence": ">=", "value": 0.90},
                actions=[Action.QUARANTINE, Action.ALERT],
                priority=100,
            ),
            PolicyRule(
                name="low-confidence-log",
                description="Log low-confidence events for review",
                event_type="*",
                conditions={"confidence": "<", "value": 0.70},
                actions=[Action.LOG],
                priority=10,
            ),
        ]

    def evaluate(self, event_type: str, confidence: float, details: dict) -> List[PolicyDecision]:
        """Evaluate an event against all rules."""
        decisions = []
        for rule in sorted(self.rules, key=lambda r: -r.priority):
            if not rule.enabled:
                continue
            if rule.event_type != "*" and rule.event_type != event_type:
                continue
            if self._check_conditions(rule.conditions, confidence):
                for action in rule.actions:
                    decision = PolicyDecision(
                        rule_name=rule.name,
                        action=action,
                        reason=f"Matched rule: {rule.description}",
                        event_details=details,
                    )
                    decisions.append(decision)
                    self.decision_log.append(decision)
                break  # First matching rule wins
        return decisions

    def _check_conditions(self, conditions: dict, confidence: float) -> bool:
        op = conditions.get("confidence")
        val = conditions.get("value", 0)
        if op == ">=":
            return confidence >= val
        elif op == ">":
            return confidence > val
        elif op == "<":
            return confidence < val
        return False

    def add_rule(self, rule: PolicyRule):
        self.rules.append(rule)
        logger.info(f"Policy rule added: {rule.name}")

    def remove_rule(self, name: str) -> bool:
        before = len(self.rules)
        self.rules = [r for r in self.rules if r.name != name]
        return len(self.rules) < before

    def get_rules(self) -> List[dict]:
        return [
            {"name": r.name, "event_type": r.event_type, "actions": [a.value for a in r.actions], "enabled": r.enabled}
            for r in self.rules
        ]
