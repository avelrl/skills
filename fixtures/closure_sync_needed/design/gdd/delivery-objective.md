# Delivery Objective

## Status

- **Document Status**: Integrated
- **System Index Status**: integrated

## Overview

The current MVP loop uses a relay gate plus deadline pressure as the delivery objective. Defeat the interceptor, reach the unlocked gate before the timer expires, and either extract or fail cleanly.

## Acceptance Criteria

- [ ] The relay gate stays locked until the interceptor is defeated.
- [ ] The countdown creates real pressure before the extraction window closes.
- [ ] Reaching the gate after unlock ends the run in a win state.
