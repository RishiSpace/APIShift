from typing import List, Dict, Any, Union
from .exceptions import RateLimitError, QuotaExceededError, NoAvailableProvidersError
from .providers import LLMProvider, GeminiProvider, OpenRouterProvider, GroqProvider

class Conversation:
    """
    Manages a conversation across multiple LLM providers.
    
    This class handles conversation history, provider switching, 
    and API interactions across different LLM providers.
    """
    
    def __init__(
        self, 
        providers: List[LLMProvider] = None, 
        max_history_length: int = 20
    ):
        """
        Initialize the conversation.
        
        :param providers: List of LLM providers to use
        :param max_history_length: Maximum number of messages to retain in history
        """
        self.providers = providers or []
        self.max_history_length = max_history_length
        self.history: List[Dict[str, str]] = []
        self.current_provider_index = 0
    
    def add_provider(self, provider: LLMProvider):
        """
        Add a new provider to the conversation.
        
        :param provider: LLM provider to add
        """
        self.providers.append(provider)
    
    def _get_current_provider(self) -> LLMProvider:
        """
        Get the current active provider.
        
        :return: Current LLM provider
        :raises NoAvailableProvidersError: If no providers are available
        """
        if not self.providers:
            raise NoAvailableProvidersError()
        
        return self.providers[self.current_provider_index]
    
    def _switch_provider(self):
        """
        Switch to the next available provider.
        
        :raises NoAvailableProvidersError: If no providers are available
        """
        if len(self.providers) <= 1:
            raise NoAvailableProvidersError()
        
        # Remove current provider if it has exhausted all keys
        if len(self.providers[self.current_provider_index].api_keys) == 1:
            del self.providers[self.current_provider_index]
            self.current_provider_index %= len(self.providers)
        else:
            # Rotate to next key
            self.providers[self.current_provider_index].rotate_key()
        
        # Move to next provider
        self.current_provider_index = (self.current_provider_index + 1) % len(self.providers)
    
    def send_message(
        self, 
        message: str, 
        **kwargs
    ) -> str:
        """
        Send a message and get a response.
        
        :param message: User message to send
        :param kwargs: Additional arguments for generation
        :return: LLM response
        :raises NoAvailableProvidersError: If no providers are available
        """
        # Add user message to history
        user_message = {"role": "user", "content": message}
        self.history.append(user_message)
        
        # Trim history if exceeding max length
        if len(self.history) > self.max_history_length:
            self.history = self.history[-self.max_history_length:]
        
        # Attempt to get response, with provider switching
        attempts = 0
        max_attempts = len(self.providers) * 2  # Each provider gets 2 attempts
        
        while attempts < max_attempts:
            try:
                # Get current provider
                current_provider = self._get_current_provider()
                
                # Generate response
                response = current_provider.generate_response(
                    messages=self.history, 
                    **kwargs
                )
                
                # Add assistant response to history
                assistant_response = {"role": "assistant", "content": response}
                self.history.append(assistant_response)
                
                return response
            
            except (RateLimitError, QuotaExceededError):
                # Switch provider on rate limit or quota error
                self._switch_provider()
                attempts += 1
        
        # If all providers fail
        raise NoAvailableProvidersError()
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get the current conversation history.
        
        :return: List of message dictionaries
        """
        return self.history.copy()
    
    def clear_history(self):
        """
        Clear the conversation history.
        """
        self.history.clear()