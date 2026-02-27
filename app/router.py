from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.index.local import LocalIndex

import warnings
warnings.filterwarnings("ignore")

ef = HuggingFaceEncoder(
    name = "sentence-transformers/all-MiniLM-L6-v2"
)

faq = Route(
    name = 'faq',
    utterances = [
        "What is the return policy of the products?",
        "Do I get discount with the HDFC credit card?",
        "Any discounts available?",
        "Is there any Discounts?",
        "How can I track my order?",
        "What payment methods are accepted?",
        "How long does it take to process a refund?",
        "Can I return a product?",
        "How do I return an item I purchased?",
        "What are your return rules?",
        "How long do I have to return something?",
        "Do you accept returns for size issues?",
        "What if my product is defective?",
        "How do you handle damaged items?",
        "Can I return a faulty product?",
        "What is your replacement policy?",
        "What to do if the item has a manufacturing defect?",
        "Do you accept returns for broken products?",
        "How can I get a refund for a damaged order?",
        "Is exchange available for defective items?",
        "What's your policy on damaged deliveries?",
        "Can I get a replacement for a faulty product?",
        "How do I report a defective order?",
        "What happens if a product doesn't work?",
        "Is there warranty support for faulty goods?",
        "Do you refund for damaged goods?",
        "How do returns work for damaged products?",
        "What is the return process for defective items?",
        "Can I raise a complaint for a damaged product?",
        "Is a product return free for manufacturing defects?",
        "What are the rules for returning faulty items?",
        "I received a broken item. What should I do?",
        "Do you offer international shipping?",
        "How do I use a promo code during checkout?",
        "How do I apply a coupon code?",
        "How to use promo code?",
        "What should I do with my promo code?"
    ],
    score_threshold=0.35
)

sql = Route(
    name = 'sql',
    utterances = [
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
        "I want to buy something.",
        "Show me products.",
        "Search for items.",
        "Find available products.",
        "What items are in stock?",
        "Browse footwear.",
        "Show clothing collection.",
        "Explore new arrivals.",
        "Show discounted items.",
        "What can I buy under Rs. 5000?",
        "Show formal pants for work.",
        "Do you have office trousers?",
        "Men's jeans under Rs. 3000.",
        "Show cotton shirts on sale.",
        "Are there any jackets on discount?",
        "Women's dresses under Rs. 2000.",
        "Buy casual shirts.",
        "Show office wear collection.",
        "Find black trousers.",
        "Show latest fashion items.",
        "Show shoes under Rs. 2000.",
        "Any sneakers below Rs. 4000?",
        "Find footwear between Rs. 3000 and Rs. 6000.",
        "What are the cheapest running shoes?",
        "Show premium shoes above Rs. 8000.",
        "Budget friendly formal shoes.",
        "Affordable leather shoes.",
        "Best shoes under 5k.",
        "Shoes in mid range price.",
        "Top rated shoes under Rs. 7000."
    ],
    score_threshold=0.35
)

small_talk = Route(
    name = 'small_talk',
    utterances = [
        "How are you?",
        "What is your name?",
        "Are you a robot?",
        "What are you?",
        "What do you do?",
        "Where are you from",
        "Who are you?",
        "Can you introduce yourself?",
        "What should I call you?",
        "Are you an AI?",
        "Are you human?",
        "Are you a chatbot?",
        "What kind of assistant are you?",
        "What’s your purpose?",
        "What are you designed for?",
        "Who created you?",
        "What can you help me with?",
        "What are your features?",
        "What services do you provide?",
        "How can you assist me?",
        "Can you answer my questions?",
        "Can you help me shop?",
        "Where were you built?",
        "Which company made you?",
        "Do you live on the internet?",
        "Are you always online?",
        "Do you have emotions?",
        "Do you learn from users?",
        "How do you work?",
        "What technology do you use?"
    ],
    score_threshold = 0.35
)
routes = [faq, sql, small_talk]

router = SemanticRouter(
    encoder = ef,
    routes = routes,
    index = LocalIndex(),
    auto_sync = 'local'
)

if __name__ == "__main__":
    print(router("give me the list of nike shoes in pink colour in less than 10k pricing.").name)
    print(router("formal shoes for work").name)
    print(router("who is your owner?").name)
    # help(Route)