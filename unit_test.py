import asyncio
import aiohttp
import json

# Base URLs for the services
SERVICE1_URL = ""
SERVICE2_URL = ""

# eg:---SERVICE1_URL = "https://ide-bbfeeedbcaf332013968deeebdeeafecbone.premiumproject.examly.io/proxy/8080/"
# eg:---SERVICE2_URL = "https://ide-bbfeeedbcaf332013968deeebdeeafecbone.premiumproject.examly.io/proxy/8081/"
class TestMicroservicesIntegration:
    
    # SERVICE 1 TESTS
    
    @staticmethod
    async def test_service1_create_and_get_student():
        """Test Service 1: Create and retrieve student"""
        async with aiohttp.ClientSession() as session:
            student_data = {
                "student_id": "s1_test001",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@test.com",
                "phone": "123-456-7890"
            }
            
            # Create student
            async with session.post(f"{SERVICE1_URL}/students", json=student_data) as response:
                assert response.status == 201
                created_student = await response.json()
                assert created_student["student_id"] == "s1_test001"
                assert created_student["first_name"] == "John"
            
            # Get student
            async with session.get(f"{SERVICE1_URL}/students/s1_test001") as response:
                assert response.status == 200
                retrieved_student = await response.json()
                assert retrieved_student["first_name"] == "John"
                assert retrieved_student["email"] == "john.doe@test.com"

    @staticmethod
    async def test_service1_update_student():
        """Test Service 1: Update student information"""
        async with aiohttp.ClientSession() as session:
            # Create student
            student_data = {
                "student_id": "s1_test002",
                "first_name": "Alice",
                "last_name": "Smith",
                "email": "alice.smith@test.com"
            }
            
            async with session.post(f"{SERVICE1_URL}/students", json=student_data) as response:
                assert response.status == 201
            
            # Update student
            updated_data = {
                "student_id": "s1_test002",
                "first_name": "Alice",
                "last_name": "Johnson",
                "email": "alice.johnson@test.com",
                "phone": "555-123-4567",
                "address": "123 Main St"
            }
            
            async with session.put(f"{SERVICE1_URL}/students/s1_test002", json=updated_data) as response:
                assert response.status == 200
                updated_student = await response.json()
                assert updated_student["last_name"] == "Johnson"
                assert updated_student["phone"] == "555-123-4567"
                assert updated_student["address"] == "123 Main St"

    @staticmethod
    async def test_service1_delete_student():
        """Test Service 1: Delete student"""
        async with aiohttp.ClientSession() as session:
            # Create student
            student_data = {
                "student_id": "s1_test003",
                "first_name": "Bob",
                "last_name": "Wilson",
                "email": "bob.wilson@test.com"
            }
            
            async with session.post(f"{SERVICE1_URL}/students", json=student_data) as response:
                assert response.status == 201
            
            # Delete student
            async with session.delete(f"{SERVICE1_URL}/students/s1_test003") as response:
                assert response.status == 204
            
            # Verify deletion
            async with session.get(f"{SERVICE1_URL}/students/s1_test003") as response:
                assert response.status == 404

    @staticmethod
    async def test_service1_list_students():
        """Test Service 1: List all students"""
        async with aiohttp.ClientSession() as session:
            # Create multiple students
            students = [
                {
                    "student_id": "s1_test004",
                    "first_name": "Emma",
                    "last_name": "Davis",
                    "email": "emma.davis@test.com"
                },
                {
                    "student_id": "s1_test005",
                    "first_name": "Mike",
                    "last_name": "Brown",
                    "email": "mike.brown@test.com"
                }
            ]
            
            for student in students:
                async with session.post(f"{SERVICE1_URL}/students", json=student) as response:
                    assert response.status == 201
            
            # List all students
            async with session.get(f"{SERVICE1_URL}/students") as response:
                assert response.status == 200
                all_students = await response.json()
                assert "s1_test004" in all_students
                assert "s1_test005" in all_students

    @staticmethod
    async def test_service1_error_handling():
        """Test Service 1: Error handling for non-existent student"""
        async with aiohttp.ClientSession() as session:
            # Try to get non-existent student
            async with session.get(f"{SERVICE1_URL}/students/nonexistent") as response:
                assert response.status == 404
            
            # Try to update non-existent student
            update_data = {
                "student_id": "nonexistent",
                "first_name": "Test",
                "last_name": "User",
                "email": "test@test.com"
            }
            async with session.put(f"{SERVICE1_URL}/students/nonexistent", json=update_data) as response:
                assert response.status == 404
            
            # Try to delete non-existent student
            async with session.delete(f"{SERVICE1_URL}/students/nonexistent") as response:
                assert response.status == 404

    # SERVICE 2 TESTS
    
    @staticmethod
    async def test_service2_create_academic_record():
        """Test Service 2: Create academic record for existing student"""
        async with aiohttp.ClientSession() as session:
            # First create a student in Service 1
            student_data = {
                "student_id": "s2_test001",
                "first_name": "Sarah",
                "last_name": "Connor",
                "email": "sarah.connor@test.com"
            }
            
            async with session.post(f"{SERVICE1_URL}/students", json=student_data) as response:
                assert response.status == 201
            
            # Create academic record in Service 2
            academic_data = {
                "student_id": "s2_test001",
                "courses": ["Math", "Physics", "Chemistry"],
                "grades": {"Math": 95.0, "Physics": 88.5, "Chemistry": 92.0},
                "enrollment_status": "active"
            }
            
            async with session.post(f"{SERVICE2_URL}/students/s2_test001/academic", json=academic_data) as response:
                assert response.status == 201
                academic_record = await response.json()
                assert academic_record["student_id"] == "s2_test001"
                assert "Math" in academic_record["courses"]
                assert academic_record["grades"]["Math"] == 95.0
                assert academic_record["enrollment_status"] == "active"

    @staticmethod
    async def test_service2_get_academic_record():
        """Test Service 2: Get academic record"""
        async with aiohttp.ClientSession() as session:
            # Create student in Service 1
            student_data = {
                "student_id": "s2_test002",
                "first_name": "Tom",
                "last_name": "Hardy",
                "email": "tom.hardy@test.com"
            }
            
            async with session.post(f"{SERVICE1_URL}/students", json=student_data) as response:
                assert response.status == 201
            
            # Create academic record
            academic_data = {
                "student_id": "s2_test002",
                "courses": ["Biology", "History"],
                "grades": {"Biology": 89.0, "History": 93.5},
                "enrollment_status": "active"
            }
            
            async with session.post(f"{SERVICE2_URL}/students/s2_test002/academic", json=academic_data) as response:
                assert response.status == 201
            
            # Get academic record
            async with session.get(f"{SERVICE2_URL}/students/s2_test002/academic") as response:
                assert response.status == 200
                academic_record = await response.json()
                assert academic_record["student_id"] == "s2_test002"
                assert set(academic_record["courses"]) == {"Biology", "History"}
                assert academic_record["grades"]["Biology"] == 89.0

    @staticmethod
    async def test_service2_update_academic_record():
        """Test Service 2: Update academic record"""
        async with aiohttp.ClientSession() as session:
            # Create student
            student_data = {
                "student_id": "s2_test003",
                "first_name": "Lisa",
                "last_name": "Wang",
                "email": "lisa.wang@test.com"
            }
            
            async with session.post(f"{SERVICE1_URL}/students", json=student_data) as response:
                assert response.status == 201
            
            # Create academic record
            academic_data = {
                "student_id": "s2_test003",
                "courses": ["Math"],
                "grades": {"Math": 85.0},
                "enrollment_status": "active"
            }
            
            async with session.post(f"{SERVICE2_URL}/students/s2_test003/academic", json=academic_data) as response:
                assert response.status == 201
            
            # Update academic record
            updated_academic_data = {
                "student_id": "s2_test003",
                "courses": ["Math", "Physics", "Computer Science"],
                "grades": {"Math": 88.0, "Physics": 91.5, "Computer Science": 96.0},
                "enrollment_status": "active"
            }
            
            async with session.put(f"{SERVICE2_URL}/students/s2_test003/academic", json=updated_academic_data) as response:
                assert response.status == 200
                updated_record = await response.json()
                assert len(updated_record["courses"]) == 3
                assert "Computer Science" in updated_record["courses"]
                assert updated_record["grades"]["Physics"] == 91.5

    @staticmethod
    async def test_service2_get_complete_student_info():
        """Test Service 2: Get complete student information (personal + academic)"""
        async with aiohttp.ClientSession() as session:
            # Create student
            student_data = {
                "student_id": "s2_test004",
                "first_name": "David",
                "last_name": "Kim",
                "email": "david.kim@test.com",
                "phone": "999-888-7777"
            }
            
            async with session.post(f"{SERVICE1_URL}/students", json=student_data) as response:
                assert response.status == 201
            
            # Create academic record
            academic_data = {
                "student_id": "s2_test004",
                "courses": ["Engineering", "Statistics"],
                "grades": {"Engineering": 94.0, "Statistics": 87.5},
                "enrollment_status": "active"
            }
            
            async with session.post(f"{SERVICE2_URL}/students/s2_test004/academic", json=academic_data) as response:
                assert response.status == 201
            
            # Get complete info
            async with session.get(f"{SERVICE2_URL}/students/s2_test004/complete") as response:
                assert response.status == 200
                complete_info = await response.json()
                
                # Verify personal info
                assert complete_info["personal_info"]["first_name"] == "David"
                assert complete_info["personal_info"]["phone"] == "999-888-7777"
                
                # Verify academic info
                assert complete_info["academic_info"]["courses"] == ["Engineering", "Statistics"]
                assert complete_info["academic_info"]["grades"]["Engineering"] == 94.0

    @staticmethod
    async def test_service2_error_handling():
        """Test Service 2: Error handling for non-existent students"""
        async with aiohttp.ClientSession() as session:
            # Try to create academic record for non-existent student
            academic_data = {
                "student_id": "nonexistent",
                "courses": ["Math"],
                "grades": {"Math": 95.0},
                "enrollment_status": "active"
            }
            
            async with session.post(f"{SERVICE2_URL}/students/nonexistent/academic", json=academic_data) as response:
                assert response.status == 404
            
            # Try to get academic record for non-existent student
            async with session.get(f"{SERVICE2_URL}/students/nonexistent/academic") as response:
                assert response.status == 404
            
            # Try to get complete info for non-existent student
            async with session.get(f"{SERVICE2_URL}/students/nonexistent/complete") as response:
                assert response.status == 404

    @classmethod
    async def cleanup_test_data(cls):
        """Clean up all test data after tests"""
        async with aiohttp.ClientSession() as session:
            # All test student IDs used in tests
            test_ids = [
                "s1_test001", "s1_test002", "s1_test003", "s1_test004", "s1_test005",
                "s2_test001", "s2_test002", "s2_test003", "s2_test004"
            ]
            
            for student_id in test_ids:
                # Try to delete academic record first (if exists)
                try:
                    async with session.delete(f"{SERVICE2_URL}/students/{student_id}/academic") as response:
                        pass  # Ignore response status
                except:
                    pass
                
                # Delete student from Service 1
                try:
                    async with session.delete(f"{SERVICE1_URL}/students/{student_id}") as response:
                        pass  # Ignore response status
                except:
                    pass

async def run_tests():
    """Run all tests for both services"""
    print("Starting comprehensive integration tests for both services...")
    print("Make sure both services are running:")
    print("- Service 1 (Personal Info): http://localhost:8080")
    print("- Service 2 (Academic Info): http://localhost:8081")
    print("=" * 60)
    
    test_instance = TestMicroservicesIntegration()
    passed_tests = 0
    total_tests = 10
    
    tests = [
        # Service 1 Tests
        ("Service 1: Create and Get Student", test_instance.test_service1_create_and_get_student),
        ("Service 1: Update Student", test_instance.test_service1_update_student),
        ("Service 1: Delete Student", test_instance.test_service1_delete_student),
        ("Service 1: List Students", test_instance.test_service1_list_students),
        ("Service 1: Error Handling", test_instance.test_service1_error_handling),
        
        # Service 2 Tests
        ("Service 2: Create Academic Record", test_instance.test_service2_create_academic_record),
        ("Service 2: Get Academic Record", test_instance.test_service2_get_academic_record),
        ("Service 2: Update Academic Record", test_instance.test_service2_update_academic_record),
        ("Service 2: Get Complete Info", test_instance.test_service2_get_complete_student_info),
        ("Service 2: Error Handling", test_instance.test_service2_error_handling),
    ]
    
    try:
        for test_name, test_func in tests:
            try:
                await test_func()
                print(f"✓ {test_name} - PASSED")
                passed_tests += 1
            except Exception as e:
                print(f"✗ {test_name} - FAILED: {str(e)}")
        
        print("=" * 60)
        print(f"Test Results: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED! Both services are working correctly.")
        else:
            print(f"❌ {total_tests - passed_tests} tests failed. Please check the services.")
        
    except Exception as e:
        print(f"Critical error during testing: {str(e)}")
        
    finally:
        # Cleanup test data
        await test_instance.cleanup_test_data()
        print("🧹 Test data cleaned up.")

if __name__ == "__main__":
    asyncio.run(run_tests())
