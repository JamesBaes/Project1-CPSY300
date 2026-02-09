import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Detect if running in Docker or locally
# Docker will have MPLBACKEND set to 'Agg' (non-interactive)
IN_DOCKER = os.environ.get('MPLBACKEND') == 'Agg'

# Create outputs directory
os.makedirs('outputs', exist_ok=True)

# Load the dataset
df = pd.read_csv('All_Diets.csv')

# Handle missing data (fill missing values with mean) 
#the mean of a string?
# df.fillna(df.mean(), inplace=True) 

# Calculate the average macronutrient content for each diet type
avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

# Find the top 5 protein-rich recipes for each diet type
top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)

# Add new metrics (Protein-to-Carbs ratio and Carbs-to-Fat ratio)
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']

# Print results to console
print("Average Macronutrients by Diet Type:")
print(avg_macros)
print("\nTop 5 Protein-Rich Recipes:")
print(top_protein[['Diet_type', 'Recipe_name', 'Protein(g)']].head(20))

# Visualization - Save AND show (if not in Docker)

# Bar chart for average protein
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'])
plt.title('Average Protein by Diet Type')
plt.ylabel('Average Protein (g)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/avg_protein.png')
print("✓ Saved: outputs/avg_protein.png")
if not IN_DOCKER:
    plt.show()  # Display the plot if running locally
plt.close()

# Bar chart for average carbs
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_macros.index, y=avg_macros['Carbs(g)'])
plt.title('Average Carbs by Diet Type')
plt.ylabel('Average Carbs (g)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/avg_carbs.png')
print("✓ Saved: outputs/avg_carbs.png")
if not IN_DOCKER:
    plt.show()
plt.close()

# Bar chart for average fat
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_macros.index, y=avg_macros['Fat(g)'])
plt.title('Average Fat by Diet Type')
plt.ylabel('Average Fat (g)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/avg_fat.png')
print("✓ Saved: outputs/avg_fat.png")
if not IN_DOCKER:
    plt.show()
plt.close()

# Heatmap to show the relationship between macronutrient content and diet types
plt.figure(figsize=(10, 8))
sns.heatmap(avg_macros, annot=True, vmin=0, vmax=150, fmt=".0f", cmap='coolwarm')
plt.title('Macronutrient Correlation Heatmap')
plt.xlabel('Macronutrient')
plt.ylabel('Diet type')
plt.tight_layout()
plt.savefig('outputs/heatmap.png')
print("✓ Saved: outputs/heatmap.png")
if not IN_DOCKER:
    plt.show()
plt.close()

# Scatter plot to display the top 5 protein-rich recipes
plt.figure(figsize=(12, 6))
sns.scatterplot(data=top_protein, x='Diet_type', y='Protein(g)', hue='Diet_type', s=100)
plt.title('Top 5 protein-rich recipes and their distribution across different cuisines')
plt.ylabel('Protein(g)')
plt.xlabel('Diet type')
plt.legend(title='Diet Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/scatter_protein.png')
print("✓ Saved: outputs/scatter_protein.png")
if not IN_DOCKER:
    plt.show()
plt.close()

print("\nAll visualizations saved to outputs/ directory!")
if IN_DOCKER:
    print("(Running in Docker - plots saved but not displayed)")
else:
    print("(Running locally - plots displayed and saved)")