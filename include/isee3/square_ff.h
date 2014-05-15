/* -*- c++ -*- */
/* 
 * Copyright 2014 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */


#ifndef INCLUDED_ISEE3_SQUARE_FF_H
#define INCLUDED_ISEE3_SQUARE_FF_H

#include <isee3/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace isee3 {

    /*!
     * \brief <+description of block+>
     * \ingroup isee3
     *
     */
    class ISEE3_API square_ff : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<square_ff> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of isee3::square_ff.
       *
       * To avoid accidental use of raw pointers, isee3::square_ff's
       * constructor is in a private implementation
       * class. isee3::square_ff::make is the public interface for
       * creating new instances.
       */
      static sptr make();
    };

  } // namespace isee3
} // namespace gr

#endif /* INCLUDED_ISEE3_SQUARE_FF_H */

