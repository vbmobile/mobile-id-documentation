# Name Match

Name Match is a feature that allows you to do a names match comparison between a candidate and a reference names (first and last/second name). It uses a combination of algorithms to compare names and return matches based on a strategy.

This strategy might be one of these two options:

- Exact (The names are identical)
- Approximate (Compare names must contain or be equal to the reference names)


=== "Android"

    ```kotlin
    /**
     * Compares a reference name against a provided name using ICAO Doc 9303
     * MRZ character transliteration rules.
     *
     * This method does not require SDK initialization.
     *
     * @param reference The name from the reference document (e.g. passport MRZ)
     * @param compare   The name to compare against the reference
     * @param strategy  [NameMatchStrategy.EXACT] or [NameMatchStrategy.APPROXIMATE]
     * @return true if names match according to the chosen strategy
     */
    fun matchNames(
        reference: Name,
        compare: Name,
        strategy: NameMatchStrategy
    ): Boolean

    /**
    * Represents a person's name with first and last name components.
    *
    * @property firstName The given/first name(s)
    * @property lastName  The family/last name(s)
    */
    data class Name(
        val firstName: String,
        val lastName: String
    )

    /**
    * Comparison strategy for name matching.
    */
    enum class NameMatchStrategy {
        /** Both names must be exactly equal after ICAO Doc 9303 sanitization. */
        EXACT,
        /** Reference names must contain or be equal to the provided names after sanitization. */
        APPROXIMATE
    }
    ```

=== "iOS"

    Work in progress...


## Usage example

=== "Android"

    ```kotlin
    val referenceName = Name(
        firstName = "JOHN", 
        lastName = "DOE"
    )
    val compareName = Name(
        firstName = "JOHN", 
        lastName = "DOE"
    )
    val isExactMatch = Enrolment.getInstance().matchNames(
        reference = referenceName, 
        compare = compareName, 
        strategy = NameMatchStrategy.EXACT
    )
    val isApproximateMatch = Enrolment.getInstance().matchNames(
        reference = referenceName, 
        compare = compareName, 
        strategy = NameMatchStrategy.APPROXIMATE
    )
    ```

=== "iOS"

    Work in progress...