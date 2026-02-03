1. Problem Statement
The current manual process for onboarding and decommissioning hardware assets is prone to data silos, inconsistent naming conventions, and delayed visibility within the organization. While the long-term goal is a network-triggered automation (fetching serial numbers upon connection), the immediate need is a robust intermediary system to standardize asset creation and Configuration Item (CI) mapping without relying on a live CMDB platform like ServiceFirst.

2. Solution Overview
This project implements an automated pipeline that ingests bulk asset data via standardized templates, enforces organizational naming standards, generates sequential identifiers, and prepares data for discovery tool integration.

3. Core Functional Requirements
Phase 1: Data Ingestion & Validation
Bulk Upload: Support for Excel-based ingestion containing critical hardware metadata:

Serial Number, Model ID, Model Category, Location, IP Address, and MAC Address.

Automated Identifier Generation:

Asset ID: System must auto-generate a unique, sequential Asset ID following organizational logic (e.g., AST-2026-0001).

CI Name Construction: Automatically derive the CI Name using a concatenation of [Model Name] + [Location Code].

CI Number: Generate a unique Configuration Item number mapped 1:1 to the Asset ID.

Phase 2: Data Mapping & Storage
Relational Mapping: The system must map the Physical Asset record to the Logical CI record, ensuring IP and MAC addresses are bound to the correct hardware profile.

Centralized Dashboard: A lightweight, web-based interface to store and visualize asset records, mimicking the functionality of a Tier-1 Service Management platform.

Phase 3: External Integration
DMR/Discovery Ready: Once a record is validated and stored, the system must expose the data (via API or export) to Digital Media Receiver (DMR) / Discovery tools.

Network Scanning: Trigger the discovery tool to scan the newly registered IP addresses to verify the asset's live status on the network.

4. Proposed Workflow
Input: User uploads a .xlsx file with raw hardware details.

Processing: * Validate for duplicate Serial Numbers.

Apply naming logic for CI naming.

Increment the Global Asset Counter for new IDs.

Output: * Data is committed to the internal database.

A summary report is generated for the user.

The Dashboard reflects the "In-Stock" or "Active" status.
