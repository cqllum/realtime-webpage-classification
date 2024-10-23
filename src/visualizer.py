# src/visualizer.py
##########################################################################
# File: visualizer.py                                                    #
# Description: Generates word clouds for visualizing text data.          #
# Author: cqllum                                                         #
# Date: 2024-10-23                                                       #
##########################################################################
# NOTE! THIS IS NOT IN USE YET, MAYBE IN LATER VERSIONS FOR WEB SUMMARY  #
##########################################################################

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io

def generate_word_cloud(text):
    """Generate a word cloud image from the provided text."""
    # Create a WordCloud instance
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Create a bytes buffer to save the image
    img_buffer = io.BytesIO()
    
    # Plot the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Hide axes
    plt.savefig(img_buffer, format='png')
    plt.close()  # Close the plot to free up memory
    
    img_buffer.seek(0)  # Rewind the buffer to the beginning
    return img_buffer.getvalue()  # Return bytes of the image
