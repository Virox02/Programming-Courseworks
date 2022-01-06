// HashMapTests.cpp
//
// ICS 45C Fall 2021
// Project #3: Maps and Legends
//
// Write unit tests for your HashMap class here.  I've provided a few tests
// already, though I've commented them out, because they won't compile and
// link until you've implemented some things.
//
// Of course, you'll want to write lots more of these tests yourself, because
// this is an inexpensive way to know whether things are working the way
// you expect -- including scenarios that you won't happen to hit in the
// course of testing your overall program.  (You might also want to be sure
// that your HashMap implementation is complete and correct before you try
// to write the rest of the program around it, anyway; there's a very
// substantial amount of partial credit available if all that works is
// HashMap.)

#include <gtest/gtest.h>
#include "HashMap.hpp"


TEST(HashMapTests, sizeOfNewlyCreatedHashMapIsZero)
{
    HashMap empty;
    ASSERT_EQ(0, empty.size());
}


TEST(HashMapTests, emptyMapContainsNoKeys)
{
    HashMap empty;
    ASSERT_FALSE(empty.contains("first"));
    ASSERT_FALSE(empty.contains("second"));
}

TEST(HashMapTests, correctValueAssociatedToTheKey)
{
    HashMap hm;
    hm.add("Viraj", "vir123");
    ASSERT_EQ("vir123", hm.value("Viraj"));
}

TEST(HashMapTests, adding5CredentialsShouldHaveSize5)
{
    HashMap hm;
    hm.add("Viraj", "123vir");
    hm.add("Boo", "123boo");
    hm.add("Alvinn", "alv345");
    hm.add("James", "jam890");
    hm.add("Sam", "567s3am");
    ASSERT_EQ(5, hm.size());
}


TEST(HashMapTests, containKeyAfterAddingIt)
{
    HashMap hm;
    hm.add("Boo", "perfect");
    ASSERT_TRUE(hm.contains("Boo"));
}

TEST(HashMapTests, copyConstructorShouldHaveSameSizeKeyValue)
{
    HashMap hm1;
    hm1.add("Viraj", "123vir");
    HashMap hm2 = hm1;
    ASSERT_EQ(hm1.size(), hm2.size());
    ASSERT_EQ(hm1.contains("Viraj"), hm2.contains("Viraj"));
    ASSERT_EQ(hm1.value("123vir"), hm2.value("vir123"));
}

TEST(HashMapTests, adding2CredentialsAndRemoving1ShouldHaveSize1)
{
    HashMap hm;
    hm.add("Viraj", "vir123");
    hm.add("Boo", "perfect");
    hm.remove("Viraj");
    ASSERT_EQ(1, hm.size());
}

TEST(HashMapTests, loadFactorShouldBe1Over5For2CredentialsAnd4Buckets)
{
    HashMap hm;
    hm.add("Viraj", "123vir");
    hm.add("Boo", "123boo");
    ASSERT_EQ(0.2, hm.loadFactor());
}

TEST(HashMapTests, allBucketsShouldBeClearedSo0Buckets)
{
    HashMap hm;
    hm.add("Viraj", "vir123");
    hm.clearbuckets();
    ASSERT_EQ(0, hm.size());
}

