import pytest
from src.optimizer import PromptOptimizer

def test_prompt_optimizer_enhancement():
    enhanced, neg = PromptOptimizer.optimize("a cybernetic samurai")
    assert "cybernetic samurai" in enhanced
    assert "photorealistic" in enhanced or "8k" in enhanced
    assert "blurry" in neg
    assert "watermark" in neg

def test_prompt_optimizer_empty():
    enhanced, neg = PromptOptimizer.optimize("")
    assert len(enhanced) > 5
    assert len(neg) > 5

def test_prompt_optimizer_no_duplicate_terms():
    base = "a sunset, highly detailed, 8k resolution"
    enhanced, _ = PromptOptimizer.optimize(base)
    # Shouldn't repeat 'highly detailed' twice
    assert enhanced.count("highly detailed") == 1
