import unittest
from multi_llm_manager import Conversation
from multi_llm_manager import GeminiProvider, OpenRouterProvider

class TestConversation(unittest.TestCase):
    def setUp(self):
        # Note: Replace with actual test API keys or mock providers
        gemini_keys = ['test_gemini_key']
        openrouter_keys = ['test_openrouter_key']
        
        self.conversation = Conversation([
            GeminiProvider(gemini_keys),
            OpenRouterProvider(openrouter_keys)
        ])
    
    def test_send_message(self):
        # This is a placeholder test
        try:
            response = self.conversation.send_message("Hello, test!")
            self.assertIsNotNone(response)
        except Exception as e:
            self.fail(f"send_message raised {type(e).__name__} unexpectedly!")

if __name__ == '__main__':
    unittest.main()
