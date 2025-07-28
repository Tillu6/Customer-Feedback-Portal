#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Customer Feedback Portal
Tests all API endpoints, data models, sentiment analysis, and database operations
"""

import requests
import json
import uuid
from datetime import datetime
import time

# Backend URL from environment
BACKEND_URL = "https://3e947a1f-ee0f-4feb-87b7-b96f314d2f52.preview.emergentagent.com/api"

class BackendTester:
    def __init__(self):
        self.test_results = []
        self.created_feedback_ids = []
        
    def log_test(self, test_name, success, message, details=None):
        """Log test results"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details:
            print(f"   Details: {details}")
    
    def test_api_root(self):
        """Test API root endpoint"""
        try:
            response = requests.get(f"{BACKEND_URL}/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    self.log_test("API Root Endpoint", True, "Root endpoint accessible", data)
                    return True
                else:
                    self.log_test("API Root Endpoint", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("API Root Endpoint", False, f"HTTP {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("API Root Endpoint", False, f"Connection error: {str(e)}")
            return False
    
    def test_create_feedback(self):
        """Test POST /api/feedback endpoint with various scenarios"""
        test_cases = [
            {
                "name": "Valid Positive Feedback",
                "data": {
                    "customer_name": "Alice Johnson",
                    "customer_email": "alice.johnson@email.com",
                    "category": "product",
                    "rating": 5,
                    "comment": "This product is absolutely amazing and wonderful! I love it so much."
                },
                "expected_sentiment": "positive"
            },
            {
                "name": "Valid Negative Feedback", 
                "data": {
                    "customer_name": "Bob Smith",
                    "customer_email": "bob.smith@email.com",
                    "category": "service",
                    "rating": 2,
                    "comment": "The service was terrible and disappointing. Really bad experience."
                },
                "expected_sentiment": "negative"
            },
            {
                "name": "Valid Neutral Feedback",
                "data": {
                    "customer_name": "Carol Davis",
                    "customer_email": "carol.davis@email.com", 
                    "category": "support",
                    "rating": 3,
                    "comment": "The support was okay, nothing special but functional."
                },
                "expected_sentiment": "neutral"
            },
            {
                "name": "Overall Category Feedback",
                "data": {
                    "customer_name": "David Wilson",
                    "customer_email": "david.wilson@email.com",
                    "category": "overall",
                    "rating": 4,
                    "comment": "Great overall experience with excellent customer service."
                },
                "expected_sentiment": "positive"
            }
        ]
        
        success_count = 0
        for test_case in test_cases:
            try:
                response = requests.post(f"{BACKEND_URL}/feedback", json=test_case["data"])
                if response.status_code == 200:
                    feedback = response.json()
                    
                    # Validate response structure
                    required_fields = ['id', 'customer_name', 'customer_email', 'category', 'rating', 'comment', 'timestamp', 'sentiment_score']
                    missing_fields = [field for field in required_fields if field not in feedback]
                    
                    if missing_fields:
                        self.log_test(f"Create Feedback - {test_case['name']}", False, f"Missing fields: {missing_fields}")
                        continue
                    
                    # Validate UUID format
                    try:
                        uuid.UUID(feedback['id'])
                        uuid_valid = True
                    except ValueError:
                        uuid_valid = False
                    
                    # Validate sentiment score
                    sentiment_score = feedback.get('sentiment_score', 0)
                    sentiment_valid = -1 <= sentiment_score <= 1
                    
                    # Check sentiment direction
                    expected_sentiment = test_case["expected_sentiment"]
                    sentiment_correct = True
                    if expected_sentiment == "positive" and sentiment_score <= 0:
                        sentiment_correct = False
                    elif expected_sentiment == "negative" and sentiment_score >= 0:
                        sentiment_correct = False
                    elif expected_sentiment == "neutral" and abs(sentiment_score) > 0.5:
                        sentiment_correct = False
                    
                    if uuid_valid and sentiment_valid and sentiment_correct:
                        self.created_feedback_ids.append(feedback['id'])
                        self.log_test(f"Create Feedback - {test_case['name']}", True, 
                                    f"Created successfully with sentiment {sentiment_score:.2f}", 
                                    f"ID: {feedback['id']}")
                        success_count += 1
                    else:
                        issues = []
                        if not uuid_valid: issues.append("Invalid UUID")
                        if not sentiment_valid: issues.append(f"Invalid sentiment score: {sentiment_score}")
                        if not sentiment_correct: issues.append(f"Incorrect sentiment direction")
                        self.log_test(f"Create Feedback - {test_case['name']}", False, f"Validation failed: {', '.join(issues)}")
                else:
                    self.log_test(f"Create Feedback - {test_case['name']}", False, f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_test(f"Create Feedback - {test_case['name']}", False, f"Error: {str(e)}")
        
        return success_count == len(test_cases)
    
    def test_invalid_feedback_creation(self):
        """Test feedback creation with invalid data"""
        invalid_cases = [
            {
                "name": "Invalid Rating (0)",
                "data": {
                    "customer_name": "Test User",
                    "customer_email": "test@email.com",
                    "category": "product",
                    "rating": 0,  # Invalid: below 1
                    "comment": "Test comment"
                }
            },
            {
                "name": "Invalid Rating (6)",
                "data": {
                    "customer_name": "Test User",
                    "customer_email": "test@email.com", 
                    "category": "product",
                    "rating": 6,  # Invalid: above 5
                    "comment": "Test comment"
                }
            },
            {
                "name": "Invalid Category",
                "data": {
                    "customer_name": "Test User",
                    "customer_email": "test@email.com",
                    "category": "invalid_category",
                    "rating": 3,
                    "comment": "Test comment"
                }
            },
            {
                "name": "Missing Required Field",
                "data": {
                    "customer_name": "Test User",
                    # Missing customer_email
                    "category": "product",
                    "rating": 3,
                    "comment": "Test comment"
                }
            }
        ]
        
        success_count = 0
        for test_case in invalid_cases:
            try:
                response = requests.post(f"{BACKEND_URL}/feedback", json=test_case["data"])
                if response.status_code in [400, 422]:  # Expected validation error
                    self.log_test(f"Invalid Data Validation - {test_case['name']}", True, 
                                f"Correctly rejected with HTTP {response.status_code}")
                    success_count += 1
                else:
                    self.log_test(f"Invalid Data Validation - {test_case['name']}", False, 
                                f"Should have been rejected but got HTTP {response.status_code}")
            except Exception as e:
                self.log_test(f"Invalid Data Validation - {test_case['name']}", False, f"Error: {str(e)}")
        
        return success_count == len(invalid_cases)
    
    def test_get_all_feedback(self):
        """Test GET /api/feedback endpoint"""
        try:
            response = requests.get(f"{BACKEND_URL}/feedback")
            if response.status_code == 200:
                feedback_list = response.json()
                if isinstance(feedback_list, list):
                    # Check if our created feedback is in the list
                    found_count = 0
                    for feedback_id in self.created_feedback_ids:
                        if any(f.get('id') == feedback_id for f in feedback_list):
                            found_count += 1
                    
                    self.log_test("Get All Feedback", True, 
                                f"Retrieved {len(feedback_list)} feedback entries, found {found_count}/{len(self.created_feedback_ids)} created entries")
                    return True
                else:
                    self.log_test("Get All Feedback", False, "Response is not a list", type(feedback_list))
                    return False
            else:
                self.log_test("Get All Feedback", False, f"HTTP {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Get All Feedback", False, f"Error: {str(e)}")
            return False
    
    def test_get_feedback_stats(self):
        """Test GET /api/feedback/stats endpoint"""
        try:
            response = requests.get(f"{BACKEND_URL}/feedback/stats")
            if response.status_code == 200:
                stats = response.json()
                required_fields = ['total_feedback', 'avg_rating', 'category_breakdown', 'rating_distribution', 'recent_feedback']
                missing_fields = [field for field in required_fields if field not in stats]
                
                if missing_fields:
                    self.log_test("Get Feedback Stats", False, f"Missing fields: {missing_fields}")
                    return False
                
                # Validate data types and ranges
                validations = []
                if not isinstance(stats['total_feedback'], int) or stats['total_feedback'] < 0:
                    validations.append("Invalid total_feedback")
                
                if not isinstance(stats['avg_rating'], (int, float)) or not (0 <= stats['avg_rating'] <= 5):
                    validations.append("Invalid avg_rating")
                
                if not isinstance(stats['category_breakdown'], dict):
                    validations.append("Invalid category_breakdown")
                
                if not isinstance(stats['rating_distribution'], dict):
                    validations.append("Invalid rating_distribution")
                
                if not isinstance(stats['recent_feedback'], list):
                    validations.append("Invalid recent_feedback")
                
                if validations:
                    self.log_test("Get Feedback Stats", False, f"Validation errors: {', '.join(validations)}")
                    return False
                
                self.log_test("Get Feedback Stats", True, 
                            f"Stats retrieved: {stats['total_feedback']} total, avg rating {stats['avg_rating']:.2f}")
                return True
            else:
                self.log_test("Get Feedback Stats", False, f"HTTP {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Get Feedback Stats", False, f"Error: {str(e)}")
            return False
    
    def test_get_feedback_by_category(self):
        """Test GET /api/feedback/category/{category} endpoint"""
        categories = ["product", "service", "support", "overall"]
        success_count = 0
        
        for category in categories:
            try:
                response = requests.get(f"{BACKEND_URL}/feedback/category/{category}")
                if response.status_code == 200:
                    feedback_list = response.json()
                    if isinstance(feedback_list, list):
                        # Verify all feedback in the list belongs to the requested category
                        category_match = all(f.get('category') == category for f in feedback_list)
                        if category_match:
                            self.log_test(f"Get Feedback by Category - {category}", True, 
                                        f"Retrieved {len(feedback_list)} feedback entries for {category}")
                            success_count += 1
                        else:
                            self.log_test(f"Get Feedback by Category - {category}", False, 
                                        "Some feedback entries don't match the requested category")
                    else:
                        self.log_test(f"Get Feedback by Category - {category}", False, 
                                    "Response is not a list", type(feedback_list))
                else:
                    self.log_test(f"Get Feedback by Category - {category}", False, 
                                f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_test(f"Get Feedback by Category - {category}", False, f"Error: {str(e)}")
        
        return success_count == len(categories)
    
    def test_delete_feedback(self):
        """Test DELETE /api/feedback/{feedback_id} endpoint"""
        if not self.created_feedback_ids:
            self.log_test("Delete Feedback", False, "No feedback IDs available for deletion testing")
            return False
        
        # Test deleting a valid feedback ID
        feedback_id_to_delete = self.created_feedback_ids[0]
        try:
            response = requests.delete(f"{BACKEND_URL}/feedback/{feedback_id_to_delete}")
            if response.status_code == 200:
                result = response.json()
                if "message" in result:
                    self.log_test("Delete Feedback - Valid ID", True, 
                                f"Successfully deleted feedback {feedback_id_to_delete}")
                    
                    # Verify it's actually deleted by trying to get all feedback
                    time.sleep(1)  # Brief delay for database consistency
                    get_response = requests.get(f"{BACKEND_URL}/feedback")
                    if get_response.status_code == 200:
                        feedback_list = get_response.json()
                        still_exists = any(f.get('id') == feedback_id_to_delete for f in feedback_list)
                        if not still_exists:
                            self.log_test("Delete Feedback - Verification", True, "Feedback successfully removed from database")
                        else:
                            self.log_test("Delete Feedback - Verification", False, "Feedback still exists in database")
                    
                    # Remove from our tracking list
                    self.created_feedback_ids.remove(feedback_id_to_delete)
                    delete_valid_success = True
                else:
                    self.log_test("Delete Feedback - Valid ID", False, "Invalid response format", result)
                    delete_valid_success = False
            else:
                self.log_test("Delete Feedback - Valid ID", False, f"HTTP {response.status_code}", response.text)
                delete_valid_success = False
        except Exception as e:
            self.log_test("Delete Feedback - Valid ID", False, f"Error: {str(e)}")
            delete_valid_success = False
        
        # Test deleting a non-existent feedback ID
        fake_id = str(uuid.uuid4())
        try:
            response = requests.delete(f"{BACKEND_URL}/feedback/{fake_id}")
            if response.status_code == 404:
                self.log_test("Delete Feedback - Invalid ID", True, "Correctly returned 404 for non-existent ID")
                delete_invalid_success = True
            else:
                self.log_test("Delete Feedback - Invalid ID", False, 
                            f"Should return 404 but got HTTP {response.status_code}")
                delete_invalid_success = False
        except Exception as e:
            self.log_test("Delete Feedback - Invalid ID", False, f"Error: {str(e)}")
            delete_invalid_success = False
        
        return delete_valid_success and delete_invalid_success
    
    def test_sentiment_analysis(self):
        """Test sentiment analysis functionality with specific test cases"""
        sentiment_test_cases = [
            {
                "comment": "This is absolutely amazing and wonderful! I love it so much. Great product!",
                "expected_range": (0.5, 1.0),
                "description": "Highly Positive"
            },
            {
                "comment": "This is terrible and awful. I hate it completely. Worst experience ever!",
                "expected_range": (-1.0, -0.5),
                "description": "Highly Negative"
            },
            {
                "comment": "The product is good but could be better.",
                "expected_range": (0.0, 0.5),
                "description": "Mildly Positive"
            },
            {
                "comment": "Not great, somewhat disappointing experience.",
                "expected_range": (-0.5, 0.0),
                "description": "Mildly Negative"
            },
            {
                "comment": "The item arrived on time and works as expected.",
                "expected_range": (-0.2, 0.2),
                "description": "Neutral"
            }
        ]
        
        success_count = 0
        for i, test_case in enumerate(sentiment_test_cases):
            feedback_data = {
                "customer_name": f"Sentiment Tester {i+1}",
                "customer_email": f"sentiment{i+1}@test.com",
                "category": "product",
                "rating": 3,
                "comment": test_case["comment"]
            }
            
            try:
                response = requests.post(f"{BACKEND_URL}/feedback", json=feedback_data)
                if response.status_code == 200:
                    feedback = response.json()
                    sentiment_score = feedback.get('sentiment_score', 0)
                    min_score, max_score = test_case["expected_range"]
                    
                    if min_score <= sentiment_score <= max_score:
                        self.log_test(f"Sentiment Analysis - {test_case['description']}", True,
                                    f"Score {sentiment_score:.2f} within expected range [{min_score}, {max_score}]")
                        success_count += 1
                        # Track for cleanup
                        self.created_feedback_ids.append(feedback['id'])
                    else:
                        self.log_test(f"Sentiment Analysis - {test_case['description']}", False,
                                    f"Score {sentiment_score:.2f} outside expected range [{min_score}, {max_score}]")
                else:
                    self.log_test(f"Sentiment Analysis - {test_case['description']}", False,
                                f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_test(f"Sentiment Analysis - {test_case['description']}", False, f"Error: {str(e)}")
        
        return success_count == len(sentiment_test_cases)
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("=" * 80)
        print("CUSTOMER FEEDBACK PORTAL - BACKEND API TESTING")
        print("=" * 80)
        print(f"Testing Backend URL: {BACKEND_URL}")
        print()
        
        # Test sequence
        tests = [
            ("API Connectivity", self.test_api_root),
            ("Feedback Creation", self.test_create_feedback),
            ("Invalid Data Validation", self.test_invalid_feedback_creation),
            ("Get All Feedback", self.test_get_all_feedback),
            ("Get Feedback Stats", self.test_get_feedback_stats),
            ("Get Feedback by Category", self.test_get_feedback_by_category),
            ("Sentiment Analysis", self.test_sentiment_analysis),
            ("Delete Feedback", self.test_delete_feedback),
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n--- Running {test_name} Tests ---")
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                self.log_test(test_name, False, f"Test suite error: {str(e)}")
        
        # Summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Total Test Suites: {total_tests}")
        print(f"Passed Test Suites: {passed_tests}")
        print(f"Failed Test Suites: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Detailed results
        print(f"\nDetailed Results ({len(self.test_results)} individual tests):")
        passed_individual = sum(1 for r in self.test_results if r['success'])
        failed_individual = len(self.test_results) - passed_individual
        print(f"✅ Passed: {passed_individual}")
        print(f"❌ Failed: {failed_individual}")
        
        if failed_individual > 0:
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
        
        return passed_tests == total_tests

if __name__ == "__main__":
    tester = BackendTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)