from typing import Dict, List, Optional


class TrustGraphNode:
    def __init__(self, node_id: str, node_type: str, data: Dict):
        self.id = node_id
        self.type = node_type
        self.data = data
        self.trust_score = 0
        self.edges = []


class TrustGraphEdge:
    def __init__(self, source_id: str, target_id: str, relationship: str, strength: float = 0.5):
        self.source = source_id
        self.target = target_id
        self.relationship = relationship
        self.strength = strength


def build_trust_graph(
    candidate_name: str,
    skills: List[str],
    projects: List[Dict[str, str]],
    certificates: List[Dict[str, str]],
    evidence_links: Dict[str, object],
) -> Dict[str, object]:
    """Build academic trust graph with nodes and relationships."""
    
    nodes = []
    edges = []
    
    # Student node
    student_node = {
        "id": f"student_{candidate_name.replace(' ', '_')}",
        "type": "student",
        "label": candidate_name,
        "trust_score": 0,
    }
    nodes.append(student_node)
    student_id = student_node["id"]
    
    # Skill nodes
    for skill in skills:
        skill_node = {
            "id": f"skill_{skill.lower().replace(' ', '_')}",
            "type": "skill",
            "label": skill,
            "trust_score": 0,
        }
        nodes.append(skill_node)
        
        # Edge from student to skill
        edges.append({
            "source": student_id,
            "target": skill_node["id"],
            "relationship": "possesses",
        })
    
    # Project nodes
    for i, project in enumerate(projects):
        proj_name = project.get("name", f"Project_{i}")
        project_node = {
            "id": f"project_{proj_name.lower().replace(' ', '_')}_{i}",
            "type": "project",
            "label": proj_name,
            "trust_score": 0,
        }
        nodes.append(project_node)
        
        # Edge from student to project
        edges.append({
            "source": student_id,
            "target": project_node["id"],
            "relationship": "created",
        })
    
    # Certificate nodes
    for i, cert in enumerate(certificates):
        cert_name = cert.get("name", f"Certificate_{i}")
        cert_node = {
            "id": f"cert_{cert_name.lower().replace(' ', '_')}_{i}",
            "type": "certificate",
            "label": cert_name,
            "trust_score": 0,
        }
        nodes.append(cert_node)
        
        # Edge from student to certificate
        edges.append({
            "source": student_id,
            "target": cert_node["id"],
            "relationship": "obtained",
        })
    
    return {
        "nodes": nodes,
        "edges": edges,
        "total_nodes": len(nodes),
        "total_edges": len(edges),
    }
