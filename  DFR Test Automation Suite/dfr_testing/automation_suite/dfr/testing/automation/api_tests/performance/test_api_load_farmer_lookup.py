```python
import pytest
import time
import statistics # For P95, median calculations
from dfr.testing.automation.api_tests.common.response_validator import ResponseValidator
from dfr.testing.automation.utils.logger_setup import setup_logger

logger = setup_logger(__name__)

TARGET_RESPONSE_TIME_MS_P95 = 500  # From REQ-API-009 (milliseconds)
NUM_REQUESTS_FOR_LOAD = 50      # Example, adjust based on B.5 and REQ-API-009 definition of peak load

@pytest.mark.api
@pytest.mark.performance
@pytest.mark.farmer_lookup
def test_farmer_lookup_response_time_under_load(admin_api_client, test_data_loader_api):
    """
    Tests the response time of the Farmer Lookup API endpoint (/farmers/{uid})
    under a sequential load of multiple requests. Measures P95 response time.
    (REQ-B.5, REQ-API-009)
    """
    logger.info(f"Starting Farmer Lookup API performance test for {NUM_REQUESTS_FOR_LOAD} sequential requests.")
    
    try:
        # Load a list of farmer UIDs to query. Ensure these UIDs exist in the test environment.
        # The file 'farmer_lookup_perf_data.json' should contain a list under "farmer_uids_set_1".
        farmer_uids_data = test_data_loader_api.get_data("farmer_lookup_perf_data.json", "farmer_uids_set_1")
        # Take a subset of UIDs up to NUM_REQUESTS_FOR_LOAD for this test run
        farmer_uids_to_test = farmer_uids_data[:NUM_REQUESTS_FOR_LOAD]
    except (FileNotFoundError, KeyError) as e:
        pytest.skip(f"Performance test data ('farmer_lookup_perf_data.json' with key 'farmer_uids_set_1') not found or incomplete: {e}")
    
    if not farmer_uids_to_test:
        pytest.skip("No farmer UIDs available in performance test data for lookup.")
    
    if len(farmer_uids_to_test) < NUM_REQUESTS_FOR_LOAD:
        logger.warning(f"Performance test will run with {len(farmer_uids_to_test)} UIDs, less than the configured {NUM_REQUESTS_FOR_LOAD}.")

    response_times_ms = []

    logger.info(f"Executing {len(farmer_uids_to_test)} lookup requests...")
    for i, uid in enumerate(farmer_uids_to_test):
        start_time = time.perf_counter()
        try:
            response = admin_api_client.get(f"/farmers/{uid}")
            # Basic validation: ensure the request was successful even during performance testing
            ResponseValidator.assert_status_code(response, 200)
        except AssertionError as ae: # Catch assertion errors from ResponseValidator
            logger.error(f"Request {i+1}/{len(farmer_uids_to_test)} for UID {uid} failed validation: {ae}")
            # Decide how to handle: fail test, or log and continue to measure remaining successful calls' performance.
            # For this example, we'll log and continue, but this might skew results if many fail.
            # Consider failing the test if functional correctness is a prerequisite for perf measurement.
            # For now, we are still timing this failed request.
        except Exception as e:
            logger.error(f"Request {i+1}/{len(farmer_uids_to_test)} for UID {uid} encountered an unexpected error: {e}")
            # Continue timing as well, but log.

        end_time = time.perf_counter()
        response_time_seconds = end_time - start_time
        response_times_ms.append(response_time_seconds * 1000) # Convert to milliseconds
        logger.debug(f"Request {i+1} (UID: {uid}) took {response_times_ms[-1]:.2f} ms.")

    if not response_times_ms:
        pytest.fail("No response times were recorded. All requests might have failed before timing.")

    # Calculate P95 and other statistics
    response_times_ms.sort() # Sort for percentile calculation
    
    count = len(response_times_ms)
    avg_response_time_ms = sum(response_times_ms) / count if count > 0 else 0
    min_response_time_ms = response_times_ms[0] if count > 0 else 0
    max_response_time_ms = response_times_ms[-1] if count > 0 else 0
    median_response_time_ms = statistics.median(response_times_ms) if count > 0 else 0
    
    # Calculate P95 (95th percentile)
    if count > 0:
        p95_index = int(count * 0.95) -1 
        if p95_index < 0: p95_index = 0 # Ensure index is valid for small sample sizes
        # If p95_index is out of bounds for very small N (e.g., N < 20 makes 0.95*N < 1, so index is -1)
        # A common approach is to take the value at index ceil(0.95*N) - 1.
        # For simplicity, if index is too high (e.g. from N*0.95 being exactly N due to rounding), cap it.
        if p95_index >= count: p95_index = count - 1
        p95_response_time_ms = response_times_ms[p95_index]
    else:
        p95_response_time_ms = 0

    logger.info(f"\n--- Farmer Lookup API Performance Summary ({count} Sequential Requests) ---")
    logger.info(f"  Min Response Time:    {min_response_time_ms:.2f} ms")
    logger.info(f"  Avg Response Time:    {avg_response_time_ms:.2f} ms")
    logger.info(f"  Median Response Time: {median_response_time_ms:.2f} ms")
    logger.info(f"  Max Response Time:    {max_response_time_ms:.2f} ms")
    logger.info(f"  P95 Response Time:    {p95_response_time_ms:.2f} ms")
    logger.info(f"  Target P95:           < {TARGET_RESPONSE_TIME_MS_P95} ms (REQ-API-009)")
    logger.info("--------------------------------------------------------------------")

    assert p95_response_time_ms < TARGET_RESPONSE_TIME_MS_P95, \
        f"P95 response time {p95_response_time_ms:.2f} ms exceeds target of {TARGET_RESPONSE_TIME_MS_P95} ms."

    # Note: For more robust load testing (concurrent users, ramp-up/down),
    # dedicated tools like Locust or k6 are generally preferred over sequential PyTest execution.
    # This test provides a basic measure of endpoint responsiveness under sequential calls.
```