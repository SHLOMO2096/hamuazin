# Audio Danger Detection Pipeline

## Project Overview

This system is built as a multi-stage data processing pipeline for audio files, using Kafka, MongoDB, and Elasticsearch.

### Flow Description

1. **Kafka Publisher Service**
   - Continuously scans a local directory of audio files.
   - Sends the file path and audio metadata (filename, size, creation date, etc.) to a Kafka topic.

2. **Kafka Consumer for MongoDB**
   - Consumes file path messages from the Kafka topic.
   - Converts the audio file’s contents to binary and stores it in MongoDB.
   - Adds a unique UUID to each document.

3. **Kafka Consumer for Elasticsearch**
   - Consumes metadata messages from the Kafka topic (in a different consumer group).
   - Adds a UUID to each record and sends the metadata to Elasticsearch.

4. **Transcription & Danger Assessment Service**
   - Loads all documents from MongoDB.
   - Transcribes each audio file (speech-to-text).
   - Performs a danger assessment on the transcript (calculates `bds_percent`, risk level, etc.).
   - Updates the corresponding document in Elasticsearch by UUID with:
     - `transcript` (speech-to-text result)
     - `bds_percent` (danger percentage)
     - `is_bds` (dangerous/not dangerous flag)
     - `bds_threat_level` (risk level: none/medium/high)

---

## Why is transcription and danger assessment placed after MongoDB?

- **Separation of Concerns**  
  Transcription and danger assessment are resource-intensive tasks. By performing these steps after storing the audio data in MongoDB, we ensure fast and reliable ingestion of raw data, without blocking the pipeline due to heavy computation.
- **Scalability**  
  The transcription and assessment service can be scaled independently, allowing parallel processing and load balancing without interfering with Kafka or MongoDB consumers.
- **Reliability**  
  If transcription or danger assessment fails or needs to be retried, all raw audio data is already safely stored in MongoDB. This enables reprocessing without any data loss.
- **Logical Structure**  
  Each service in the pipeline has a clear responsibility: one handles ingesting and storing raw data, the other performs advanced processing and enrichment before updating Elasticsearch.

---

## Summary

Placing the transcription and danger assessment service after MongoDB ensures a flexible, robust, and maintainable pipeline. This design supports scalability, error handling, and clear separation between ingestion, storage, and enrichment stages.