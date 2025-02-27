from typing import Dict, List
from src.indexer import DocumentIndexer

class CDPChatbot:
    def __init__(self):
        self.indexer = DocumentIndexer()
        self.indexer.load_documents()
        
        # Define CDP platforms we support
        self.supported_cdps = ["segment", "mparticle", "lytics", "zeotap"]
        
        # Define comparison keywords
        self.comparison_keywords = [
            "compare", "comparison", "versus", "vs", "difference", "differences",
            "better", "best", "prefer", "advantage", "disadvantage"
        ]
        
    def answer_question(self, question: str) -> str:
        """
        Answers a user's question about CDPs
        """
        # Handle extremely long questions
        if len(question) > 500:
            question = self._truncate_question(question)
            
        # Check if question is CDP-related
        if not self._is_cdp_related(question):
            return "I'm a CDP Support chatbot. I can only answer questions related to Customer Data Platforms (CDPs) like Segment, mParticle, Lytics, or Zeotap. Please ask me how to perform specific tasks within these platforms."
        
        # Check if it's a comparison question
        if self._is_comparison_question(question):
            return self._handle_comparison_question(question)
            
        # Identify which CDP the question is about
        cdp = self._identify_cdp(question)
            
        # Search for relevant documentation
        try:
            results = self.indexer.search(question)
            
            if not results:
                return f"I couldn't find specific information about that. Could you please rephrase your question? Try asking how to perform a specific task in {', '.join(self.supported_cdps)}."
                
            # Format the response
            response = self._format_response(results, cdp)
            return response
            
        except Exception as e:
            # Handle any errors during search
            print(f"Error during search: {str(e)}")
            return f"I'm having trouble processing that question. Could you please try rephrasing it or asking about a different topic?"
        
    def _truncate_question(self, question: str) -> str:
        """
        Truncates extremely long questions to a manageable length
        while preserving the core question
        """
        # Try to find the actual question part (often at the end)
        question_markers = ["?", "how", "what", "where", "when", "why", "who", "which", "can", "could"]
        
        for marker in question_markers:
            if marker in question.lower():
                # Find the last occurrence of the marker
                pos = question.lower().rfind(marker)
                if pos > len(question) // 2:  # If it's in the latter half
                    # Extract from a bit before the marker to the end
                    start_pos = max(0, pos - 50)
                    return question[start_pos:]
        
        # If no clear question marker, just take the last part
        return question[-300:]
        
    def _is_cdp_related(self, question: str) -> bool:
        """
        Checks if the question is related to CDPs
        """
        question_lower = question.lower()
        
        # Check for CDP platform names
        for cdp in self.supported_cdps:
            if cdp in question_lower:
                return True
                
        # Check for CDP-related keywords
        cdp_keywords = [
            'customer data platform', 'cdp', 'integration', 'source', 'audience',
            'segment', 'profile', 'tracking', 'analytics', 'data collection',
            'identity resolution', 'user profile', 'event tracking', 'api',
            'webhook', 'destination', 'data source', 'user data'
        ]
        
        for keyword in cdp_keywords:
            if keyword in question_lower:
                return True
                
        # Check for "how to" questions that might be CDP-related
        how_to_patterns = ['how to', 'how do i', 'how can i', 'steps to', 'guide for']
        action_verbs = ['create', 'set up', 'configure', 'integrate', 'connect', 'track', 'implement']
        
        for pattern in how_to_patterns:
            if pattern in question_lower:
                for verb in action_verbs:
                    if verb in question_lower:
                        return True
                        
        return False
        
    def _identify_cdp(self, question: str) -> str:
        """
        Identifies which CDP the question is about
        Returns the identified CDP or None if unclear
        """
        question_lower = question.lower()
        
        # Check for specific phrases that might cause confusion
        segmentation_phrases = [
            "audience segment", 
            "user segment",
            "customer segment",
            "segment your audience",
            "segment your users",
            "segment your customers"
        ]
        
        # If the question is about audience segmentation and mentions a CDP other than Segment,
        # prioritize that CDP
        if any(phrase in question_lower for phrase in segmentation_phrases):
            for cdp in self.supported_cdps:
                if cdp != "segment" and cdp in question_lower:
                    return cdp
        
        # For all other cases, check each CDP
        for cdp in self.supported_cdps:
            # Special handling for "segment" to avoid confusion with "audience segment"
            if cdp == "segment":
                # Check if it's a standalone word or part of a CDP-related context
                import re
                segment_patterns = [
                    r'\bsegment\b',  # segment as a standalone word
                    r'segment\s+cdp',  # segment CDP
                    r'segment\s+platform'  # segment platform
                ]
                
                # Skip if it's likely part of "audience segment" and not the CDP
                if any(phrase in question_lower for phrase in segmentation_phrases):
                    continue
                    
                for pattern in segment_patterns:
                    if re.search(pattern, question_lower):
                        return cdp
            elif cdp in question_lower:
                return cdp
                
        return None
    
    def _is_comparison_question(self, question: str) -> bool:
        """
        Determines if the question is asking for a comparison between CDPs
        """
        question_lower = question.lower()
        
        # Check for specific phrases that should not be treated as comparisons
        non_comparison_phrases = [
            "audience segment", 
            "user segment",
            "customer segment",
            "segment your audience",
            "segment your users",
            "segment your customers"
        ]
        
        # If the question contains any of these phrases, it's likely about segmentation, not a comparison
        for phrase in non_comparison_phrases:
            if phrase in question_lower:
                # Check if there are explicit comparison keywords that would override this
                explicit_comparison = False
                for keyword in ["compare", "versus", "vs", "difference between"]:
                    if keyword in question_lower:
                        explicit_comparison = True
                        break
                
                if not explicit_comparison:
                    return False
        
        # Check for comparison keywords first
        for keyword in self.comparison_keywords:
            if keyword in question_lower:
                return True
                
        # Check for specific comparison patterns
        comparison_patterns = [
            r"how does .+ compare to",
            r"difference between .+ and",
            r"which is better .+ or",
            r"which cdp is better",
            r".+ vs .+"
        ]
        
        import re
        for pattern in comparison_patterns:
            if re.search(pattern, question_lower):
                return True
                
        # Check if at least two CDPs are mentioned
        # But be careful with "segment" which could be part of "audience segment"
        mentioned_cdps = []
        for cdp in self.supported_cdps:
            # For "segment", make sure it's not part of "audience segment", etc.
            if cdp == "segment":
                # Check if it's a standalone word or part of a CDP-related context
                segment_patterns = [
                    r'\bsegment\b',  # segment as a standalone word
                    r'segment\s+cdp',  # segment CDP
                    r'segment\s+platform'  # segment platform
                ]
                
                for pattern in segment_patterns:
                    if re.search(pattern, question_lower):
                        mentioned_cdps.append(cdp)
                        break
            elif cdp in question_lower:
                mentioned_cdps.append(cdp)
        
        if len(mentioned_cdps) >= 2:
            return True
                
        return False
    
    def _handle_comparison_question(self, question: str) -> str:
        """
        Handles questions comparing different CDPs
        """
        question_lower = question.lower()
        
        # Identify which CDPs are being compared
        mentioned_cdps = [cdp for cdp in self.supported_cdps if cdp in question_lower]
        
        if len(mentioned_cdps) < 2:
            # If fewer than 2 CDPs are explicitly mentioned, try to infer from context
            # Look for patterns like "difference between X and" to find the second CDP
            import re
            for cdp in self.supported_cdps:
                if cdp not in mentioned_cdps:
                    patterns = [
                        f"difference between {cdp} and",
                        f"difference between .+ and {cdp}",
                        f"{cdp} vs",
                        f"vs {cdp}",
                        f"compare .+ to {cdp}",
                        f"compare {cdp} to"
                    ]
                    for pattern in patterns:
                        if re.search(pattern, question_lower):
                            mentioned_cdps.append(cdp)
                            break
            
            # If still fewer than 2 CDPs, use the most relevant ones based on the question
            if len(mentioned_cdps) < 2:
                # For simplicity, we'll use the first two CDPs
                # In a real implementation, we would use more sophisticated relevance scoring
                remaining_cdps = [cdp for cdp in self.supported_cdps if cdp not in mentioned_cdps]
                mentioned_cdps.extend(remaining_cdps[:2-len(mentioned_cdps)])
        
        # Limit to just 2 CDPs for clearer comparison
        mentioned_cdps = mentioned_cdps[:2]
        
        # Identify the feature or functionality being compared
        comparison_features = self._extract_comparison_features(question)
        
        # Search for relevant documentation for each CDP
        all_results = []
        for cdp in mentioned_cdps:
            # Create a CDP-specific query
            cdp_query = f"{comparison_features} in {cdp}"
            results = self.indexer.search(cdp_query)
            if results:
                all_results.append((cdp, results[0]))  # Take the best match for each CDP
        
        # Format the comparison response
        if not all_results:
            return f"I don't have enough information to compare {' and '.join(mentioned_cdps)} regarding {comparison_features}. Could you please ask a more specific question?"
        
        response = f"Here's a comparison of {comparison_features} between {' and '.join(mentioned_cdps)}:\n\n"
        
        for cdp, result in all_results:
            doc = result['document']
            response += f"**{cdp.title()}**:\n"
            
            # Extract relevant content (shortened for readability)
            content = doc['content']
            if len(content) > 300:
                # Try to extract the most relevant part
                sentences = content.split('.')
                relevant_sentences = []
                for sentence in sentences:
                    if any(feature in sentence.lower() for feature in comparison_features.split()):
                        relevant_sentences.append(sentence)
                
                if relevant_sentences:
                    content = '. '.join(relevant_sentences[:3]) + '.'
                else:
                    content = content[:300] + "..."
            
            response += content + "\n\n"
        
        # Add a comparison summary
        response += "**Key Differences**:\n"
        if len(all_results) >= 2:
            # Extract some basic differences based on the content
            response += "- " + self._generate_difference_point(all_results[0][0], all_results[1][0], comparison_features) + "\n"
        
        response += "\nNote: This comparison is based on the available documentation. For more detailed comparisons, you may want to consult each platform's full documentation."
        
        return response
    
    def _extract_comparison_features(self, question: str) -> str:
        """
        Extracts the features or functionality being compared
        """
        question_lower = question.lower()
        
        # Common CDP features that might be compared
        features = [
            "audience creation", "audience segmentation", "data collection", 
            "integration", "identity resolution", "user profiles", "event tracking",
            "api", "performance", "pricing", "ease of use", "implementation",
            "data sources", "destinations", "connectors", "sdks", "security",
            "compliance", "data governance", "reporting", "analytics"
        ]
        
        # Check for these features in the question
        found_features = []
        for feature in features:
            if feature in question_lower:
                found_features.append(feature)
        
        if found_features:
            return ", ".join(found_features)
            
        # Check for specific comparison patterns
        import re
        comparison_patterns = {
            r"difference between": "general capabilities",
            r"which is better for (.+?)\?": None,  # Group 1 will be the feature
            r"compare .+ for (.+)": None,  # Group 1 will be the feature
            r"how do .+ compare in (.+)": None,  # Group 1 will be the feature
        }
        
        for pattern, default_feature in comparison_patterns.items():
            match = re.search(pattern, question_lower)
            if match and default_feature is None and match.groups():
                # Extract the feature from the regex group
                return match.group(1).strip()
            elif match and default_feature:
                return default_feature
        
        # If no specific features found, extract nouns as potential features
        # Remove CDP names and comparison keywords from the question
        cleaned_question = question_lower
        for cdp in self.supported_cdps:
            cleaned_question = cleaned_question.replace(cdp, "")
        for keyword in self.comparison_keywords:
            cleaned_question = cleaned_question.replace(keyword, "")
        
        # Extract potential feature words (nouns)
        words = re.findall(r'\b[a-z]{4,}\b', cleaned_question)  # Simple heuristic: words with 4+ chars
        if words:
            # Filter out common stop words
            stop_words = ["what", "which", "when", "where", "there", "their", "about", "would", "should", "could", "between"]
            filtered_words = [word for word in words if word not in stop_words]
            if filtered_words:
                return "data integration and capabilities"  # Default to a common comparison point
        
        return "features and capabilities"  # Default if nothing specific found
    
    def _generate_difference_point(self, cdp1: str, cdp2: str, feature: str) -> str:
        """
        Generates a comparison point between two CDPs
        This is a simplified implementation that could be enhanced with more detailed knowledge
        """
        # Some pre-defined comparison points based on common knowledge
        comparisons = {
            ("segment", "mparticle", "audience"): f"{cdp1.title()} focuses on data collection and routing, while {cdp2.title()} has more advanced audience segmentation capabilities.",
            ("segment", "mparticle", "integration"): f"{cdp1.title()} has a wider range of integrations, while {cdp2.title()} offers deeper mobile-specific integrations.",
            ("segment", "lytics", "audience"): f"{cdp1.title()} requires more technical setup, while {cdp2.title()} offers more marketer-friendly audience creation tools.",
            ("mparticle", "lytics", "audience"): f"{cdp1.title()} excels in mobile data collection, while {cdp2.title()} focuses on content affinity and predictive modeling.",
            ("zeotap", "segment", "identity"): f"{cdp1.title()} has stronger identity resolution capabilities, while {cdp2.title()} offers more flexible data routing options.",
            ("zeotap", "mparticle", "general"): f"{cdp1.title()} specializes in cross-channel identity resolution and data unification, while {cdp2.title()} excels in mobile data collection and offers a more developer-friendly interface.",
            ("zeotap", "mparticle", "integration"): f"{cdp1.title()} uses a connection-based approach with detailed data mapping, while {cdp2.title()} offers a more streamlined integration process through their dashboard.",
            ("zeotap", "mparticle", "identity"): f"{cdp1.title()} provides more robust identity resolution rules for cross-channel data, while {cdp2.title()} focuses on creating comprehensive user profiles with automatic event association.",
            ("zeotap", "mparticle", "features"): f"{cdp1.title()} is better suited for enterprises with complex data environments, while {cdp2.title()} is stronger for companies with significant mobile presence.",
            ("zeotap", "mparticle", "capabilities"): f"{cdp1.title()} offers more detailed configuration options for data connections, while {cdp2.title()} provides a simpler interface for basic data collection needs.",
        }
        
        # Check for pre-defined comparisons
        for (c1, c2, f), comparison in comparisons.items():
            if ((cdp1 == c1 and cdp2 == c2) or (cdp1 == c2 and cdp2 == c1)) and (f in feature or "general" == f or "features" == f or "capabilities" == f):
                if cdp1 != c1:  # Swap the comparison if the order is different
                    comparison = comparison.replace(c1.title(), "TEMP").replace(c2.title(), c1.title()).replace("TEMP", c2.title())
                return comparison
        
        # Generate a generic comparison if no specific one is found
        return f"{cdp1.title()} and {cdp2.title()} have different approaches to {feature}, with each offering unique advantages depending on your specific use case."
        
    def _format_response(self, results: List[Dict], cdp: str = None) -> str:
        """
        Formats the search results into a coherent response
        """
        if not results:
            return f"I couldn't find specific information about that. Could you please rephrase your question?"
            
        best_match = results[0]['document']
        
        # If CDP wasn't identified in the question, use the one from the best match
        if not cdp:
            cdp = best_match['cdp']
            
        # Start with a friendly introduction
        response = f"Here's how to do that in {cdp.title()}:\n\n"
        
        # Extract the most relevant content
        content = best_match['content']
        
        # If the content is too long, try to extract the most relevant part
        if len(content) > 800:
            # Look for sections that might contain steps or instructions
            step_indicators = ["Step 1", "1.", "First", "To begin", "Start by"]
            
            for indicator in step_indicators:
                if indicator in content:
                    # Find the position of the indicator
                    pos = content.find(indicator)
                    # Extract from that position onwards (up to a reasonable length)
                    content = content[pos:pos+800] + "..."
                    break
            else:
                # If no step indicators found, just truncate
                content = content[:800] + "..."
        
        # Add the content to the response
        response += content + "\n\n"
        
        # Add a source reference
        response += f"Source: {best_match['url']}"
        
        # If we have more results, offer them as additional resources
        if len(results) > 1:
            response += "\n\nYou might also find these resources helpful:\n"
            for i, result in enumerate(results[1:3], 1):  # Add up to 2 more resources
                doc = result['document']
                response += f"{i}. {doc['title'] if 'title' in doc and doc['title'] else 'Additional resource'}: {doc['url']}\n"
        
        return response 