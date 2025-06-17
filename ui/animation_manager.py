"""
Animation manager for handling animations in the game
"""
import pygame
import math

class Animation:
    def __init__(self, duration, loop=False, callback=None):
        self.duration = duration  # Duration in seconds
        self.elapsed = 0
        self.loop = loop
        self.callback = callback
        self.finished = False
        self.paused = False
        
    def update(self, dt):
        """Update the animation
        
        Args:
            dt: Time delta in seconds
            
        Returns:
            float: Progress from 0.0 to 1.0
        """
        if self.paused or self.finished:
            return self.get_progress()
            
        self.elapsed += dt
        
        if self.elapsed >= self.duration:
            if self.loop:
                self.elapsed %= self.duration
            else:
                self.elapsed = self.duration
                self.finished = True
                if self.callback:
                    self.callback()
                    
        return self.get_progress()
        
    def get_progress(self):
        """Get the current progress of the animation
        
        Returns:
            float: Progress from 0.0 to 1.0
        """
        if self.duration == 0:
            return 1.0
        return min(1.0, self.elapsed / self.duration)
        
    def reset(self):
        """Reset the animation"""
        self.elapsed = 0
        self.finished = False
        
    def pause(self):
        """Pause the animation"""
        self.paused = True
        
    def resume(self):
        """Resume the animation"""
        self.paused = False


class EasingAnimation(Animation):
    """Animation with easing functions"""
    
    EASING_LINEAR = 0
    EASING_EASE_IN = 1
    EASING_EASE_OUT = 2
    EASING_EASE_IN_OUT = 3
    EASING_BOUNCE = 4
    EASING_ELASTIC = 5
    
    def __init__(self, duration, easing_type=0, loop=False, callback=None):
        super().__init__(duration, loop, callback)
        self.easing_type = easing_type
        
    def get_progress(self):
        """Get the current progress with easing applied
        
        Returns:
            float: Eased progress from 0.0 to 1.0
        """
        linear_progress = super().get_progress()
        
        if self.easing_type == self.EASING_LINEAR:
            return linear_progress
        elif self.easing_type == self.EASING_EASE_IN:
            return linear_progress * linear_progress
        elif self.easing_type == self.EASING_EASE_OUT:
            return 1 - (1 - linear_progress) * (1 - linear_progress)
        elif self.easing_type == self.EASING_EASE_IN_OUT:
            if linear_progress < 0.5:
                return 2 * linear_progress * linear_progress
            else:
                return 1 - pow(-2 * linear_progress + 2, 2) / 2
        elif self.easing_type == self.EASING_BOUNCE:
            if linear_progress < 1 / 2.75:
                return 7.5625 * linear_progress * linear_progress
            elif linear_progress < 2 / 2.75:
                linear_progress -= 1.5 / 2.75
                return 7.5625 * linear_progress * linear_progress + 0.75
            elif linear_progress < 2.5 / 2.75:
                linear_progress -= 2.25 / 2.75
                return 7.5625 * linear_progress * linear_progress + 0.9375
            else:
                linear_progress -= 2.625 / 2.75
                return 7.5625 * linear_progress * linear_progress + 0.984375
        elif self.easing_type == self.EASING_ELASTIC:
            if linear_progress == 0 or linear_progress == 1:
                return linear_progress
            
            p = 0.3
            s = p / 4
            return pow(2, -10 * linear_progress) * math.sin((linear_progress - s) * (2 * math.pi) / p) + 1
            
        return linear_progress


class AnimationManager:
    def __init__(self):
        self.animations = {}
        
    def add_animation(self, name, animation):
        """Add an animation
        
        Args:
            name: Name of the animation
            animation: Animation object
        """
        self.animations[name] = animation
        
    def create_animation(self, name, duration, loop=False, callback=None):
        """Create and add a new animation
        
        Args:
            name: Name of the animation
            duration: Duration in seconds
            loop: Whether to loop the animation
            callback: Function to call when animation finishes
            
        Returns:
            Animation: The created animation
        """
        animation = Animation(duration, loop, callback)
        self.add_animation(name, animation)
        return animation
        
    def create_easing_animation(self, name, duration, easing_type=EasingAnimation.EASING_LINEAR, loop=False, callback=None):
        """Create and add a new easing animation
        
        Args:
            name: Name of the animation
            duration: Duration in seconds
            easing_type: Type of easing to apply
            loop: Whether to loop the animation
            callback: Function to call when animation finishes
            
        Returns:
            EasingAnimation: The created animation
        """
        animation = EasingAnimation(duration, easing_type, loop, callback)
        self.add_animation(name, animation)
        return animation
        
    def get_animation(self, name):
        """Get an animation by name
        
        Args:
            name: Name of the animation
            
        Returns:
            Animation: The animation or None if not found
        """
        return self.animations.get(name)
        
    def update(self, dt):
        """Update all animations
        
        Args:
            dt: Time delta in seconds
            
        Returns:
            dict: Dictionary of animation progresses
        """
        progresses = {}
        
        for name, animation in self.animations.items():
            progresses[name] = animation.update(dt)
            
        return progresses
        
    def reset_animation(self, name):
        """Reset an animation
        
        Args:
            name: Name of the animation
        """
        if name in self.animations:
            self.animations[name].reset()
            
    def reset_all(self):
        """Reset all animations"""
        for animation in self.animations.values():
            animation.reset()
            
    def remove_animation(self, name):
        """Remove an animation
        
        Args:
            name: Name of the animation
        """
        if name in self.animations:
            del self.animations[name]
