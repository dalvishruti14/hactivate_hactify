import random
from threading import Thread
from queue import Queue
import string
import itertools
from typing import List, Optional, Set, Union, Dict
import unicodedata
from unidecode import unidecode
import re

class Scout:
    def __init__(self, 
            check_variants: bool = True, 
            check_prefixes: bool = True, 
            normalize: bool = True,
            num_threads: int = 5,
            num_bulk_threads: int = 1) -> None:
        """
        Initialize the Scout object with default settings.

        Args:
            check_variants (bool): Flag to check variants. Defaults to True.
            check_prefixes (bool): Flag to check prefixes. Defaults to True.
            normalize (bool): Flag to normalize data. Defaults to True.
            num_threads (int): Number of email finder threads for concurrency. Defaults to 5.
            num_bulk_threads (int): Number of bulk email finder threads for concurrency. Defaults to 1.
        """
        
        self.check_variants = check_variants
        self.check_prefixes = check_prefixes
        self.normalize = normalize
        self.num_threads = num_threads
        self.num_bulk_threads = num_bulk_threads

    def normalize_name(self, name: str) -> str:
        """
        Convert a non-email compliant name to a normalized email-friendly format.

        Args:
        name (str): The name to be normalized.

        Returns:
        str: A normalized, email-friendly version of the name.
        """
        # Basic normalization
        name = name.upper().lower()

        # Normalize using unidecode for proper transliteration
        name = unidecode(name)

        # Normalize to NFKD form which separates characters and their diacritics
        normalized = unicodedata.normalize('NFKD', name)

        # Encode to ASCII bytes, then decode back to string ignoring non-ASCII characters
        ascii_encoded = normalized.encode('ascii', 'ignore').decode('ascii')

        # Replace any remaining non-alphanumeric characters with an empty string
        email_compliant = re.sub(r'[^a-zA-Z0-9]', '', ascii_encoded)

        return email_compliant

    def generate_prefixes(self, domain: str, custom_prefixes: Optional[List[str]] = None) -> List[str]:
        """
        Generate a list of email addresses with common or custom prefixes for a given domain.

        Args:
        domain (str): The domain for which to generate email addresses.
        custom_prefixes (List[str], optional): A list of custom prefixes. If provided, these
                                            prefixes are used instead of the common ones.

        Returns:
        List[str]: A list of email addresses with the specified prefixes.
        """
        common_prefixes = [
            # Business Prefixes
            "info", "contact", "sales", "support", "admin",
            "service", "team", "hello", "marketing", "hr",
            "office", "accounts", "billing", "careers", "jobs",
            "press", "help", "enquiries", "management", "staff",
            "webmaster", "administrator", "customer", "tech",
            "finance", "legal", "compliance", "operations", "it",
            "network", "development", "research", "design", "engineering",
            "production", "purchasing", "logistics", "training",
            "ceo", "director", "manager",
            "executive", "agent", "representative", "partner",
            # Website Management Prefixes
            "blog", "forum", "news", "updates", "events",
            "community", "shop", "store", "feedback",
            "media", "resource", "resources",
            "api", "dev", "developer", "status", "security"
        ]

        prefixes = custom_prefixes if custom_prefixes is not None else common_prefixes
        return [f"{prefix}@{domain}" for prefix in prefixes]

    def generate_email_variants(self, names: List[str], domain: str, normalize: bool = True) -> List[str]:
        """
        Generate a set of email address variants based on a list of names for a given domain.

        This function creates combinations of the provided names, both with and without dots
        between them, and also includes individual names and their first initials.

        Args:
        names (List[str]): A list of names to combine into email address variants.
        domain (str): The domain to be appended to each email variant.
        normalize (bool, optional): If True, normalize the prefixes to email-friendly format.

        Returns:
        List[str]: A list of unique email address variants.
        """
        variants: Set[str] = set()

        assert False not in [isinstance(i, str) for i in names]

        if normalize:
            normalized_names = [self.normalize_name(name) for name in names]
            names = normalized_names

        # Generate combinations of different lengths
        for r in range(1, len(names) + 1):
            for name_combination in itertools.permutations(names, r):
                # Join the names in the combination with and without a dot
                variants.add(''.join(name_combination))
                variants.add('.'.join(name_combination))

        # Add individual names (and their first initials) as variants
        for name in names:
            variants.add(name)
            variants.add(name[0])

        return [f"{variant}@{domain}" for variant in variants]

    def find_valid_emails(self,
                        domain: str, 
                        names: Optional[Union[str, List[str], List[List[str]]]] = None, 
                        )-> List[str]:
        """
        Find valid email addresses for a given domain based on various checks.

        Args:
        domain (str): The domain to check email addresses against.
        names (Union[str, List[str], List[List[str]]], optional): Names to generate email variants. 
            Can be a single string, a list of strings, or a list of lists of strings.

        Returns:
        List[str]: A list of valid email addresses found.
        """
        valid_emails = []
        email_variants = []
        generated_mails = []

        # Generate email variants based on the type of 'names'
        if self.check_variants and names:
            if isinstance(names, str):
                names = names.split(" ")
            if isinstance(names, list) and names and isinstance(names[0], list):
                for name_list in names:
                    assert isinstance(name_list, list)
                    name_list = self.split_list_data(name_list)
                    email_variants.extend(self.generate_email_variants(name_list, domain, normalize=self.normalize))
            else:
                names = self.split_list_data(names)
                email_variants = self.generate_email_variants(names, domain, normalize=self.normalize)

        if self.check_prefixes and not names:
            generated_mails = self.generate_prefixes(domain)

        all_emails = email_variants + generated_mails

        # For demonstration purposes, we'll just return the generated emails without checking SMTP or DNS
        return all_emails

    def find_valid_emails_bulk(self,
        email_data: List[Dict[str, Union[str, List[str]]]], 
        ) -> List[Dict[str, Union[str, List[str], List[Dict[str, str]]]]]:
        """
        Find valid email addresses in bulk for multiple domains and names.

        Args:
        email_data (List[Dict[str, Union[str, List[str]]]]): A list of dictionaries, 
            each containing domain and optional names to check.

        Returns:
        List[Dict[str, Union[str, List[str], List[Dict[str, str]]]]]: A list of dictionaries, 
            each containing the domain, names, and a list of valid emails found.
        """
        # Remove duplicates
        email_data_clean = [i for n, i in enumerate(email_data) if i not in email_data[n + 1:]]

        all_valid_emails = []

        for data in email_data_clean:
            domain = data.get("domain")
            names = data.get("names", [])
            valid_emails = self.find_valid_emails(domain, names)
            all_valid_emails.append({"domain": domain, "names": names, "valid_emails": valid_emails})

        return all_valid_emails
    
    def split_list_data(self, target):
        new_target = []
        for i in target:
            new_target.extend(i.split(" "))
        return new_target
