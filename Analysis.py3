# Modern, professional dashboard
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import cm
import warnings
warnings.filterwarnings('ignore')

# Set professional style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Create figure with subplots
fig = plt.figure(figsize=(20, 16))
fig.suptitle('STUDENT FEEDBACK ANALYSIS DASHBOARD\nComprehensive Course Evaluation Insights', 
            fontsize=24, fontweight='bold', y=0.98)

# Create grid for subplots
gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)

# 1. RADAR CHART - Overall Performance
ax1 = fig.add_subplot(gs[0, :2], polar=True)

# Prepare data for radar chart
categories = list(average_ratings.index)
N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

values = average_ratings.values.tolist()
values += values[:1]

ax1.plot(angles, values, 'o-', linewidth=3, label='Average Ratings', color='#FF6B6B')
ax1.fill(angles, values, alpha=0.25, color='#FF6B6B')
ax1.set_xticks(angles[:-1])
ax1.set_xticklabels(categories, fontsize=9)
ax1.set_ylim(0, 10)
ax1.set_yticklabels([])
ax1.grid(True)
ax1.set_title('Overall Performance Radar Chart', size=14, fontweight='bold', pad=20)

# 2. HEATMAP with annotations
ax2 = fig.add_subplot(gs[0, 2:])

# Create a beautiful correlation heatmap
corr_matrix = df_clean.drop(['Student ID', 'Satisfaction_Level'], axis=1, errors='ignore').corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='RdYlBu', center=0, 
           square=True, ax=ax2, cbar_kws={'shrink': 0.8},
           annot_kws={'size': 10, 'weight': 'bold'})
ax2.set_title('Aspect Correlation Matrix', fontsize=14, fontweight='bold', pad=20)

# 3. SATISFACTION DISTRIBUTION - Donut Chart
ax3 = fig.add_subplot(gs[1, 0])

colors = ['#2E8B57', '#3CB371', '#FFD700', '#FF6347']
wedges, texts, autotexts = ax3.pie(satisfaction_counts.values, 
                                  labels=satisfaction_counts.index,
                                  autopct='%1.1f%%',
                                  colors=colors,
                                  startangle=90,
                                  wedgeprops=dict(width=0.3))

# Beautify the text
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(10)

ax3.set_title('Student Satisfaction Distribution', fontsize=14, fontweight='bold')

# 4. RATING DISTRIBUTION - Violin Plot
ax4 = fig.add_subplot(gs[1, 1])

# Melt data for violin plot
melted_data = pd.melt(df_clean.drop(['Student ID', 'Satisfaction_Level'], axis=1, errors='ignore'),
                     var_name='Aspect', value_name='Rating')

sns.violinplot(data=melted_data, x='Rating', y='Aspect', palette='viridis', ax=ax4)
ax4.set_title('Rating Distribution by Aspect', fontsize=14, fontweight='bold')
ax4.grid(axis='x', alpha=0.3)

# 5. TOP & BOTTOM PERFORMERS - Horizontal Bar Chart
ax5 = fig.add_subplot(gs[1, 2:])

# Combine top and bottom aspects
top_bottom = pd.concat([average_ratings.head(3), average_ratings.tail(3)])
colors = ['#2E8B57'] * 3 + ['#FF6347'] * 3

bars = ax5.barh(range(len(top_bottom)), top_bottom.values, color=colors, alpha=0.8)
ax5.set_yticks(range(len(top_bottom)))
ax5.set_yticklabels(top_bottom.index)
ax5.set_xlabel('Average Rating')
ax5.set_title('Top Performers vs Areas for Improvement', fontsize=14, fontweight='bold')

# Add value annotations on bars
for i, (bar, value) in enumerate(zip(bars, top_bottom.values)):
    ax5.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
            f'{value:.2f}', ha='left', va='center', fontweight='bold')

# 6. TREND ANALYSIS - Line plot over student IDs (sampled)
ax6 = fig.add_subplot(gs[2, :])

# Sample students for better visualization
sample_size = min(100, len(df_clean))
sampled_df = df_clean.sample(sample_size).sort_index()

# Plot trend for key aspects
key_aspects = ['Knowledgeable', 'Clear_Explanation', 'Doubt_Solving', 'Recommendation']
for aspect in key_aspects:
    ax6.plot(sampled_df['Student ID'], sampled_df[aspect], 
            marker='o', markersize=3, linewidth=2, label=aspect, alpha=0.7)

ax6.set_xlabel('Student ID (Sampled)')
ax6.set_ylabel('Rating')
ax6.set_title('Rating Trends Across Students (Sampled)', fontsize=14, fontweight='bold')
ax6.legend()
ax6.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
