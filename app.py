
import streamlit as st
import ollama

st.set_page_config(
    page_title="SellerSpark AI",
    page_icon="🌟",
    layout="centered"
)

st.title("🌟 SellerSpark AI")
st.subheader("Turn product details into ready-to-use sales content.")
st.write(
    "An AI writing assistant for small businesses, "
    "online sellers, and side hustlers."
)

st.caption("Powered by Gemma 3 • Local AI generation")
st.divider()

# Product details
product_name = st.text_input(
    "🛍️ Product name",
    placeholder="Example: Handmade jasmine soap"
)

price = st.text_input(
    "💰 Price (optional)",
    placeholder="Example: ₹199"
)

features = st.text_area(
    "✨ Product features",
    placeholder="Example: Handmade, jasmine fragrance, gift-friendly packaging"
)

audience = st.text_input(
    "👥 Target customers",
    placeholder="Example: People looking for unique gifts"
)

# Content preferences
platform = st.selectbox(
    "📱 Where will you sell?",
    ["Instagram", "WhatsApp", "Online marketplace"]
)

language = st.selectbox(
    "🌐 Content language",
    ["English", "Telugu"]
)

tone = st.selectbox(
    "✍️ Writing style",
    ["Friendly", "Professional", "Creative", "Premium"]
)

# Generate content
if st.button("✨ Generate Sales Content", use_container_width=True):

    if not product_name.strip() or not features.strip():
        st.warning("Please enter the product name and its features.")

    else:
        prompt = f"""
You are SellerSpark AI, a truthful marketing assistant
for small businesses.

SELLER-PROVIDED INFORMATION:
Product: {product_name}
Price: {price.strip() if price.strip() else "Not provided"}
Features: {features}
Target customers: {audience.strip() if audience.strip() else "General customers"}
Platform: {platform}
Language: {language}
Tone: {tone}

Generate these sections:

1. PRODUCT TITLE
2. SHORT DESCRIPTION
3. KEY SELLING POINTS
4. SALES MESSAGE for {platform}
5. RELEVANT KEYWORDS AND HASHTAGS

STRICT RULES:
- Use only facts explicitly provided by the seller.
- Never invent ingredients, materials, benefits, quality claims,
  certifications, customer reviews, discounts, or guarantees.
- Do not assume a product is natural, organic, safe, premium,
  moisturizing, handmade, or chemical-free unless the seller
  explicitly states it.
- Do not invent a price.
- Do not add unrelated ingredients or product features.
- If information is missing, omit that claim.
- Do not include placeholder instructions or fake links.
- Use the selected language: {language}.
- Use the selected writing tone: {tone}.
- Make the message suitable for {platform}.
- Keep the output clear, concise, and ready to use.
"""

        try:
            with st.spinner("🌟 Creating your sales content..."):
                response = ollama.chat(
                    model="gemma3:1b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

            generated_content = response["message"]["content"]

            # Store the generated content in session state
            st.session_state["generated_content"] = generated_content

            st.success("Your sales content is ready!")

        except Exception as error:
            st.error(
                "Could not generate content. Please check that "
                "Ollama is running and Gemma 3 is installed."
            )
            st.caption(f"Technical details: {error}")

# Display generated content outside the button block
if st.session_state.get("generated_content"):
    generated_content = st.session_state["generated_content"]

    st.divider()
    st.subheader("📝 Your Sales Content")
    st.markdown(generated_content)

    st.divider()
    st.subheader("📋 Copy Your Content")

    st.text_area(
        "Generated content",
        value=generated_content,
        height=300,
        key="copy_content_box"
    )

    st.caption(
        "Use the copy icon inside the text box to copy your content."
    )

    st.download_button(
        label="⬇️ Download Content as TXT",
        data=generated_content,
        file_name="sellerspark_marketing_content.txt",
        mime="text/plain",
        use_container_width=True
    )

st.divider()

st.caption(
    "SellerSpark AI • Built with Streamlit, Ollama and Gemma 3"
)
