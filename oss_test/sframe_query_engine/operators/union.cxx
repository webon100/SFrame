/**
 * Copyright (C) 2015 Dato, Inc.
 * All rights reserved.
 *
 * This software may be modified and distributed under the terms
 * of the BSD license. See the LICENSE file for details.
 */
#include <sframe_query_engine/execution/execution_node.hpp>
#include <sframe_query_engine/operators/sarray_source.hpp>
#include <sframe_query_engine/operators/union.hpp>
#include <sframe/sarray.hpp>
#include <sframe/algorithm.hpp>
#include <cxxtest/TestSuite.h>

#include "check_node.hpp"

using namespace graphlab;
using namespace graphlab::query_eval;

class union_test : public CxxTest::TestSuite {
 public:

  void test_union_empty() {
    auto sa_left = std::make_shared<sarray<flexible_type>>();
    sa_left->open_for_write();
    sa_left->close();

    auto sa_right = std::make_shared<sarray<flexible_type>>();
    sa_right->open_for_write();
    sa_right->close();

    std::vector<flexible_type> expected;

    auto node = make_node(op_sarray_source(sa_left), op_sarray_source(sa_right));
    check_node(node, expected);
  }

  void test_union() {
    std::vector<flexible_type> data{0,1,2,3,4,5};
    auto sa_left = std::make_shared<sarray<flexible_type>>();
    sa_left->open_for_write();
    graphlab::copy(data.begin(), data.end(), *sa_left);
    sa_left->close();

    auto sa_right = std::make_shared<sarray<flexible_type>>();
    sa_right->open_for_write();
    graphlab::copy(data.begin(), data.end(), *sa_right);
    sa_right->close();

    std::vector<std::vector<flexible_type>> expected;
    for (auto& i : data) {
      expected.push_back(std::vector<flexible_type>{data[i], data[i]});
    }
    auto node = make_node(op_sarray_source(sa_left), op_sarray_source(sa_right));
    check_node(node, expected);
  }

 private:
  std::shared_ptr<execution_node> make_node(const op_sarray_source& source_left,
                                            const op_sarray_source& source_right) {
    auto left_node = std::make_shared<execution_node>(std::make_shared<op_sarray_source>(source_left));
    auto right_node = std::make_shared<execution_node>(std::make_shared<op_sarray_source>(source_right));
    auto node = std::make_shared<execution_node>(std::make_shared<op_union>(),
                                                 std::vector<std::shared_ptr<execution_node>>({left_node, right_node}));
    return node;
  }
};
