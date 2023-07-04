# Copyright (c) 2023 UiDOM
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from dataclasses import dataclass, field

from demosite.api import api
from demosite.document import document
from uidom.dom import *


class TestimonialGroup(Component):
    """https://tws.zarifprogrammer.com/snippets"""

    def render(self, *args, **kwargs):
        return f"""<section class="text-gray-600 body-font">
  <div class="container px-5 py-24 mx-auto">
	<h1 class="mb-12 text-3xl font-medium text-center text-gray-900 title-font">Testimonials</h1>
	<div class="flex flex-wrap -m-4">
      {args}
    </div>
	</div>
  </div>
</section>"""


@dataclass(eq=False)
class Testimonial(Component):
    image: str = field(default="https://dummyimage.com/106x106")
    name: str = field(default="Holden Caulfield")
    profession: str = field(default="UI DEVELOPER")
    description: str = field(
        default="""Synth chartreuse iPhone lomo cray raw denim brunch everyday carry neutra before 
        they sold out fixie 90's microdosing. Tacos pinterest fanny pack venmo, post-ironic heirloom try-hard pabst authentic iceland.
        """
    )

    def __post_init__(self, *args, **kwargs):
        super().__init__(
            image=self.image,
            name=self.name,
            profession=self.profession,
            description=self.description,
        )

    def render(
        self,
        image,
        name,
        profession,
        description,
    ):
        return f"""
    <div class="w-full p-4 md:w-1/2 border border-gray-500 rounded-md bg-gray-100">
      <div class="h-full p-8 bg-gray-200 rounded-md">
        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="block w-5 h-5 mb-4 text-gray-400" viewBox="0 0 975.036 975.036">
          <path d="M925.036 57.197h-304c-27.6 0-50 22.4-50 50v304c0 27.601 22.4 50 50 50h145.5c-1.9 79.601-20.4 143.3-55.4 191.2-27.6 37.8-69.399 
          69.1-125.3 93.8-25.7 11.3-36.8 41.7-24.8 67.101l36 76c11.6 24.399 40.3 35.1 65.1 24.399 66.2-28.6 122.101-64.8 167.7-108.8 55.601-53.7 
          93.7-114.3 114.3-181.9 20.601-67.6 30.9-159.8 30.9-276.8v-239c0-27.599-22.401-50-50-50zM106.036 913.497c65.4-28.5 121-64.699 166.9-108.6 
          56.1-53.7 94.4-114.1 115-181.2 20.6-67.1 30.899-159.6 30.899-277.5v-239c0-27.6-22.399-50-50-50h-304c-27.6 0-50 22.4-50 50v304c0 27.601 22.4 
          50 50 50h145.5c-1.9 79.601-20.4 143.3-55.4 191.2-27.6 37.8-69.4 69.1-125.3 93.8-25.7 11.3-36.8 41.7-24.8 67.101l35.9 75.8c11.601 24.399 
          40.501 35.2 65.301 24.399z"></path>
        </svg>
        <p class="mb-6 leading-relaxed font-montserrat">{description}</p>
        <a class="inline-flex items-center">
        <div class="flex flex-row border border-gray-500 p-2 rounded-md bg-gray-300">
          <img alt="testimonial" src={image} class="flex-shrink-0 object-cover object-center w-12 h-12 border rounded-full">
          <span class="flex flex-col flex-grow pl-4 ml-4 ">
            <span class="font-medium text-gray-900 font-montserrat ">{name}</span>
            <span class="font-medium text-sm text-gray-300 font-teko">{profession}</span>
          </span>
        </div>
        </a>
      </div>
	  </div>
    """


@api.get("/testimonials")
def testimonials():
    return document(
        Testimonial(
            image="https://dummyimage.com/107x107",
            name="Alper Kamu",
            profession="DESIGNER",
            description="Best Designer",
        ),
        Testimonial(),
    )


if __name__ == "__main__":
    print(Testimonial().get(str))
