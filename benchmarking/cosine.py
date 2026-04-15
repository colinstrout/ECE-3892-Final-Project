from sentence_transformers import SentenceTransformer, util

embedder_path = "./models/embedding_model"
embedder = SentenceTransformer(embedder_path)

summary_raven = ["the RAVEN system is an internally developed battery management platform. it provides continuous measurement of cell voltage, temperature, and discharge rates across all units. the system is deployed on our local network to ensure full control over operational data and comply with internal security requirements.", "the RAVEN system is an internally developed battery management platform. it provides continuous measurement of cell voltage, temperature, and discharge rates across all units. the system is deployed on our local network to ensure full control."]
summary_other = ["the ZEUS-X1 battery array employs a heterogeneous cell-to-pack (CTP) architecture. each cell is rated for a nominal voltage of 3.2V. the integrated thermal management system activates an active liquid-cooling loop", "the ZEUS-X1 battery array uses a heterogeneous cell-to-pack architecture. each cell rated for a nominal voltage of 3.2V. a thermal management system activates an active liquid-cooling loop."]

embeddings_raven = embedder.encode(summary_raven, convert_to_tensor=True)
cos_sim_raven = util.cos_sim(embeddings_raven[0], embeddings_raven[1])
print(f"🔍 Cosine Similarity (RAVEN): {cos_sim_raven.item():.4f}")

# Process OTHER
embeddings_other = embedder.encode(summary_other, convert_to_tensor=True)
cos_sim_other = util.cos_sim(embeddings_other[0], embeddings_other[1])
print(f"🔍 Cosine Similarity (OTHER): {cos_sim_other.item():.4f}")